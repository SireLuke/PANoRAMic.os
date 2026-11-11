"""Exact E8 lattice-shell moments and spectral/harmonic audit.

The shell generator uses the canonical E8 lattice
D8 union (D8 + (1/2,...,1/2)); coordinates are stored doubled as integers.
Moment checks are exact Fractions. NumPy is used only for bounded SVD and
symmetric graph-spectrum diagnostics.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb, prod

from core.geometry.e8_root_system import dot, e8_roots_exact


def e8_lattice_shell(n: int) -> tuple[tuple[int, ...], ...]:
    """Return doubled integer coordinates for E8 vectors of norm squared 2n."""
    if not isinstance(n, int) or n < 1 or n > 3:
        raise ValueError("initial exact shell audit supports n=1,2,3")
    target = 8 * n
    shell: set[tuple[int, ...]] = set()

    # D8: integer coordinates with even coordinate sum; doubled coordinates
    # are even and lie in {-4,-2,0,2,4} for these first three shells.
    for x in product(range(-2, 3), repeat=8):
        if sum(x) % 2 == 0 and 4 * sum(v * v for v in x) == target:
            shell.add(tuple(2 * v for v in x))

    # D8 + (1/2)^8: doubled coordinates are odd; subtracting one gives
    # twice the D8 integer shift, whose coordinate sum must be divisible by 4.
    for z in product((-3, -1, 1, 3), repeat=8):
        if sum(v * v for v in z) == target and sum(z) % 4 == 0:
            shell.add(tuple(z))

    result = tuple(sorted(shell))
    expected = {1: 240, 2: 2160, 3: 6720}[n]
    if len(result) != expected:
        raise AssertionError(f"E8 shell n={n}: expected {expected}, got {len(result)}")
    if any(sum(x * x for x in v) != target for v in result):
        raise AssertionError("shell contains a vector with incorrect norm")
    return result


def _compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in _compositions(total - first, parts - 1):
            yield (first,) + rest


def _odd_double_factorial_half(beta: int) -> int:
    value = 1
    for j in range(1, beta + 1):
        value *= 2 * j - 1
    return value


def spherical_moment_audit(n: int, max_even_degree: int = 8) -> dict:
    """Compare every even coordinate monomial moment with uniform S^7."""
    if max_even_degree not in (2, 4, 6, 8):
        raise ValueError("max_even_degree must be one of 2,4,6,8")
    shell = e8_lattice_shell(n)
    shell_set = set(shell)
    centrally_symmetric = all(tuple(-x for x in v) in shell_set for v in shell)
    if not centrally_symmetric:
        raise AssertionError("E8 shell must be centrally symmetric")

    results = {}
    for degree in range(2, max_even_degree + 1, 2):
        m = degree // 2
        sphere_denominator = prod(8 + 2 * j for j in range(m))
        mismatches = []
        checked = 0
        for beta in _compositions(m, 8):
            numerator = 0
            for vector in shell:
                term = 1
                for coordinate, exponent in zip(vector, beta):
                    if exponent:
                        term *= coordinate ** (2 * exponent)
                numerator += term
            observed = Q(numerator, len(shell) * (8 * n) ** m)
            expected = Q(
                prod(_odd_double_factorial_half(b) for b in beta),
                sphere_denominator,
            )
            checked += 1
            if observed != expected:
                mismatches.append({
                    "multi_index_half": beta,
                    "observed": str(observed),
                    "sphere": str(expected),
                })
        results[str(degree)] = {
            "even_monomials_checked": checked,
            "mismatches": len(mismatches),
            "first_mismatch": mismatches[0] if mismatches else None,
            "matches_uniform_sphere": not mismatches,
        }
    return {
        "shell_index": n,
        "point_count": len(shell),
        "squared_norm": 2 * n,
        "centrally_symmetric": centrally_symmetric,
        "odd_moments_zero_through_degree_7": centrally_symmetric,
        "even_moment_checks": results,
        "spherical_design_conclusion": (
            "exact coordinate-moment agreement through degree 7; degree 8 fails"
            if all(results[str(k)]["matches_uniform_sphere"] for k in (2, 4, 6))
            and results.get("8", {}).get("mismatches", 0) > 0
            else "see per-degree moment results"
        ),
    }


def harmonic_dimension_s7(degree: int) -> int:
    """Dimension of degree-l spherical harmonics on S^7."""
    if degree < 0:
        return 0
    return comb(degree + 7, 7) - comb(degree + 5, 7)


def polynomial_restriction_dimension_s7(max_degree: int) -> int:
    return sum(harmonic_dimension_s7(k) for k in range(max_degree + 1))


def _monomial_exponents(degree: int, variables: int = 8):
    return combinations_with_replacement(range(variables), degree)


def shell_polynomial_rank_audit(n: int, max_degree: int = 4,
                                sample_rows: int = 500,
                                seed: int = 20261111) -> dict:
    """Numerical SVD rank lower bounds for restrictions of polynomials to S^7.

    On a fixed-radius shell, homogeneous degrees l and l-1 span restrictions
    of all polynomials of degree <=l. For large shells, deterministic seeded
    row subsampling is used; full expected rank in the sample certifies the
    full shell rank, while a deficient sample is only a lower bound.
    """
    import numpy as np

    shell = e8_lattice_shell(n)
    rng = np.random.default_rng(seed + 100 * n)
    if len(shell) > sample_rows:
        chosen = np.sort(rng.choice(len(shell), size=sample_rows, replace=False))
        sample = np.asarray([shell[int(i)] for i in chosen], dtype=np.int64)
    else:
        sample = np.asarray(shell, dtype=np.int64)

    rows = []
    for degree in range(max_degree + 1):
        columns = []
        for homogeneous_degree in (degree, degree - 1):
            if homogeneous_degree < 0:
                continue
            for monomial in _monomial_exponents(homogeneous_degree):
                if homogeneous_degree == 0:
                    values = np.ones(len(sample), dtype=np.float64)
                else:
                    values = np.prod(sample[:, list(monomial)], axis=1).astype(np.float64)
                columns.append(values)
        matrix = np.column_stack(columns)
        singular_values = np.linalg.svd(matrix, compute_uv=False)
        rank = int((singular_values > singular_values[0] * 1e-9).sum())
        expected_dimension = polynomial_restriction_dimension_s7(degree)
        theoretical_max = min(len(shell), expected_dimension)
        rows.append({
            "degree_leq": degree,
            "sample_matrix_shape": list(matrix.shape),
            "numerical_rank": rank,
            "expected_restriction_dimension": expected_dimension,
            "theoretical_max_rank": theoretical_max,
            "sample_reaches_theoretical_max": rank == min(len(sample), expected_dimension),
            "full_shell_rank_certified": (
                rank == theoretical_max and len(sample) == len(shell)
            ) or (
                rank == expected_dimension and expected_dimension <= len(sample)
            ),
            "smallest_singular_value": float(singular_values[-1]),
            "rank_method": "float64 SVD; relative cutoff 1e-9",
        })
    return {"shell_index": n, "point_count": len(shell), "degrees": rows}


def _gegenbauer(degree: int, lam: int, x: Q) -> Q:
    if degree == 0:
        return Q(1)
    previous, current = Q(1), Q(2 * lam) * x
    if degree == 1:
        return current
    for k in range(1, degree):
        following = (
            Q(2 * (k + lam)) * x * current
            - Q(k + 2 * lam - 1) * previous
        ) / Q(k + 1)
        previous, current = current, following
    return current


def e8_root_graph_spectral_audit() -> dict:
    """Compare the 240-root neighbour graph spectrum with S^7 Gegenbauer data."""
    import numpy as np

    roots = e8_roots_exact()
    adjacency = np.zeros((len(roots), len(roots)), dtype=np.float64)
    for i, left in enumerate(roots):
        for j, right in enumerate(roots):
            if i != j and dot(left, right) == 1:
                adjacency[i, j] = 1.0
    degrees = adjacency.sum(axis=1)
    if not np.all(degrees == 56):
        raise AssertionError("E8 root graph must be 56-regular")
    laplacian = np.diag(degrees) - adjacency
    eigenvalues = np.linalg.eigvalsh(laplacian)
    observed = Counter(int(round(float(x))) for x in eigenvalues)
    expected_spectrum = {0: 1, 28: 8, 48: 35, 58: 112, 60: 84}
    if dict(sorted(observed.items())) != expected_spectrum:
        raise AssertionError(f"unexpected E8 root graph spectrum: {dict(observed)}")

    predictions = []
    for degree in range(5):
        at_half = _gegenbauer(degree, 3, Q(1, 2))
        at_one = _gegenbauer(degree, 3, Q(1))
        predicted = Q(56) * (1 - at_half / at_one)
        predictions.append({
            "harmonic_degree": degree,
            "gegenbauer_laplacian_eigenvalue": str(predicted),
            "observed_laplacian_eigenvalue": int(predicted),
            "observed_multiplicity": expected_spectrum[int(predicted)],
            "full_S7_harmonic_dimension": harmonic_dimension_s7(degree),
        })
    return {
        "vertices": 240,
        "degree": 56,
        "laplacian_spectrum": [
            {"eigenvalue": value, "multiplicity": multiplicity}
            for value, multiplicity in sorted(observed.items())
        ],
        "gegenbauer_comparison": predictions,
        "interpretation": (
            "multiplicities match S^7 harmonic dimensions for degrees 0..3; "
            "the degree-4 predicted eigenvalue occurs with multiplicity 84, "
            "the residual dimension after the degree<=3 restrictions (240-156)"
        ),
        "scope": "finite root-graph spectral/harmonic comparison; not a quantum model",
    }


if __name__ == "__main__":
    import json
    print(json.dumps({
        "shell_moments": [spherical_moment_audit(n) for n in (1, 2, 3)],
        "shell_polynomial_ranks": [shell_polynomial_rank_audit(n) for n in (1, 2, 3)],
        "root_graph": e8_root_graph_spectral_audit(),
    }, indent=2, sort_keys=True))
