import type { NAHTState } from "../types.ts";

export interface ComplexNumber {
  readonly re: number;
  readonly im: number;
}

export type Complex9Vector = readonly ComplexNumber[];
export type SU9Matrix = readonly (readonly ComplexNumber[])[];

const DIMENSION = 9;
const DEFAULT_TOLERANCE = 1e-10;

function assertComplex(value: ComplexNumber, label: string): void {
  if (!value || !Number.isFinite(value.re) || !Number.isFinite(value.im)) {
    throw new TypeError(label + " must have finite real and imaginary parts");
  }
}

function add(a: ComplexNumber, b: ComplexNumber): ComplexNumber {
  return { re: a.re + b.re, im: a.im + b.im };
}

function subtract(a: ComplexNumber, b: ComplexNumber): ComplexNumber {
  return { re: a.re - b.re, im: a.im - b.im };
}

function multiply(a: ComplexNumber, b: ComplexNumber): ComplexNumber {
  return { re: a.re * b.re - a.im * b.im, im: a.re * b.im + a.im * b.re };
}

function divide(a: ComplexNumber, b: ComplexNumber): ComplexNumber {
  const denominator = b.re * b.re + b.im * b.im;
  if (denominator === 0) throw new RangeError("Cannot divide by zero");
  return {
    re: (a.re * b.re + a.im * b.im) / denominator,
    im: (a.im * b.re - a.re * b.im) / denominator,
  };
}

function magnitude(a: ComplexNumber): number {
  return Math.hypot(a.re, a.im);
}

export function validateComplex9Vector(vector: Complex9Vector): void {
  if (!Array.isArray(vector) || vector.length !== DIMENSION) {
    throw new TypeError("SU(9) state must contain exactly nine complex amplitudes");
  }
  vector.forEach((value, index) => assertComplex(value, "state[" + index + "]"));
}

/** Squared Hermitian norm of a nine-component complex vector. */
export function complex9NormSquared(vector: Complex9Vector): number {
  validateComplex9Vector(vector);
  return vector.reduce((sum, value) => sum + value.re * value.re + value.im * value.im, 0);
}

function determinant(matrix: SU9Matrix): ComplexNumber {
  const rows = matrix.map((row) => row.map((value) => ({ re: value.re, im: value.im })));
  let result: ComplexNumber = { re: 1, im: 0 };
  let sign = 1;

  for (let column = 0; column < DIMENSION; column += 1) {
    let pivot = column;
    for (let row = column + 1; row < DIMENSION; row += 1) {
      if (magnitude(rows[row][column]) > magnitude(rows[pivot][column])) pivot = row;
    }
    if (magnitude(rows[pivot][column]) <= DEFAULT_TOLERANCE) {
      return { re: 0, im: 0 };
    }
    if (pivot !== column) {
      [rows[pivot], rows[column]] = [rows[column], rows[pivot]];
      sign *= -1;
    }
    const diagonal = rows[column][column];
    result = multiply(result, diagonal);
    for (let row = column + 1; row < DIMENSION; row += 1) {
      const factor = divide(rows[row][column], diagonal);
      for (let next = column + 1; next < DIMENSION; next += 1) {
        rows[row][next] = subtract(rows[row][next], multiply(factor, rows[column][next]));
      }
    }
  }
  return { re: sign * result.re, im: sign * result.im };
}

/** Validate that a complex 9x9 matrix is unitary and has determinant one. */
export function validateSU9Matrix(
  matrix: SU9Matrix,
  tolerance = DEFAULT_TOLERANCE,
): void {
  if (!Array.isArray(matrix) || matrix.length !== DIMENSION ||
      matrix.some((row) => !Array.isArray(row) || row.length !== DIMENSION)) {
    throw new TypeError("SU(9) matrix must be exactly 9 by 9");
  }
  if (!Number.isFinite(tolerance) || tolerance <= 0) {
    throw new RangeError("tolerance must be finite and positive");
  }
  for (let i = 0; i < DIMENSION; i += 1) {
    for (let j = 0; j < DIMENSION; j += 1) {
      assertComplex(matrix[i][j], "matrix[" + i + "][" + j + "]");
    }
  }

  for (let i = 0; i < DIMENSION; i += 1) {
    for (let j = 0; j < DIMENSION; j += 1) {
      let inner: ComplexNumber = { re: 0, im: 0 };
      for (let k = 0; k < DIMENSION; k += 1) {
        const conjugate = { re: matrix[k][i].re, im: -matrix[k][i].im };
        inner = add(inner, multiply(conjugate, matrix[k][j]));
      }
      const expected = i === j ? 1 : 0;
      if (Math.hypot(inner.re - expected, inner.im) > tolerance) {
        throw new RangeError("SU(9) matrix must be unitary");
      }
    }
  }

  const det = determinant(matrix);
  if (Math.hypot(det.re - 1, det.im) > tolerance * DIMENSION) {
    throw new RangeError("SU(9) matrix must have determinant one");
  }
}

/** Apply a validated SU(9) fundamental-representation action to C^9. */
export function applySU9(matrix: SU9Matrix, vector: Complex9Vector): Complex9Vector {
  validateSU9Matrix(matrix);
  validateComplex9Vector(vector);
  const output = matrix.map((row) => {
    let value: ComplexNumber = { re: 0, im: 0 };
    for (let column = 0; column < DIMENSION; column += 1) {
      value = add(value, multiply(row[column], vector[column]));
    }
    return Object.freeze(value);
  });
  return Object.freeze(output);
}

export function validateNAHTStateForSU9Projection(state: NAHTState): void {
  if (!state || typeof state.frameId !== "string" || state.frameId.length === 0 ||
      !Array.isArray(state.channels) || state.channels.length !== 3 ||
      state.channels.some((value) => !Number.isFinite(value))) {
    throw new TypeError("Projection must return a valid three-channel NAHT state");
  }
}
