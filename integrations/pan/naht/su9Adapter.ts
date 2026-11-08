import type {
  Complex9Vector,
  SU9Matrix,
} from "../../../modules/naht/src/backends/su9.ts";
import {
  applySU9,
  validateComplex9Vector,
  validateNAHTStateForSU9Projection,
  validateSU9Matrix,
} from "../../../modules/naht/src/backends/su9.ts";
import type { NAHTState, ProvenanceRecord } from "../../../modules/naht/src/types.ts";
import { validateV9Vector, type V9Vector } from "./v9Adapter.ts";

export interface V9ComplexEncoder {
  readonly id: string;
  readonly version: string;
  readonly meaning: string;
  readonly xiSemantics: string;
  readonly xiUnits: string;
  encode(vector: V9Vector): Complex9Vector;
}

export interface SU9NAHTProjection {
  readonly id: string;
  readonly version: string;
  readonly meaning: string;
  project(amplitudes: Complex9Vector): NAHTState;
}

export interface AdaptedV9SU9State {
  readonly state: NAHTState;
  readonly amplitudes: Complex9Vector;
  readonly provenance: ProvenanceRecord;
}

function requireDescriptor(value: { id: string; version: string; meaning: string; xiSemantics?: string; xiUnits?: string }, label: string): void {
  if (!value || typeof value.id !== "string" || !value.id.trim() ||
      typeof value.version !== "string" || !value.version.trim() ||
      typeof value.meaning !== "string" || !value.meaning.trim() ||
      (label === "V9 complex encoder" && (typeof value.xiSemantics !== "string" || !value.xiSemantics.trim() || typeof value.xiUnits !== "string" || !value.xiUnits.trim()))) {
    throw new TypeError(label + " requires an id, version, and meaning");
  }
}

/**
 * Versioned V9 -> C^9 encoding -> SU(9) action -> explicit NAHT projection.
 * The encoder and output projection are caller supplied; no physical mapping is implied.
 */
export function adaptV9ThroughSU9ToNAHT(
  vector: V9Vector,
  matrix: SU9Matrix,
  encoder: V9ComplexEncoder,
  projection: SU9NAHTProjection,
  sourceVersion = "PAN-V9",
): AdaptedV9SU9State {
  validateV9Vector(vector);
  validateSU9Matrix(matrix);
  requireDescriptor(encoder, "V9 complex encoder");
  requireDescriptor(projection, "SU(9)-to-NAHT projection");

  const snapshot: V9Vector = Object.freeze({
    h: vector.h, R: vector.R, u: vector.u, d: vector.d,
    tau: vector.tau, chi: vector.chi, s: vector.s, f: vector.f, xi: vector.xi,
  });
  const encoded = encoder.encode(snapshot);
  validateComplex9Vector(encoded);
  const amplitudes = applySU9(matrix, encoded);
  const projected = projection.project(amplitudes);
  validateNAHTStateForSU9Projection(projected);

  const state: NAHTState = Object.freeze({
    frameId: projected.frameId,
    channels: Object.freeze([...projected.channels]) as unknown as readonly [number, number, number],
  });
  const provenance: ProvenanceRecord = Object.freeze({
    source: "PAN-V9+SU(9)",
    sourceVersion,
    projectionId: encoder.id + "@" + encoder.version + " -> SU(9) -> " +
      projection.id + "@" + projection.version,
    attributes: Object.freeze({
      readOnly: true,
      axisCount: 9,
      complexAmplitudeCount: 9,
      channelCount: 3,
      xiSemantics: encoder.xiSemantics,
      xiUnits: encoder.xiUnits,
      encodingMeaning: encoder.meaning,
      outputProjectionMeaning: projection.meaning,
      group: "SU(9)",
    }),
  });
  return Object.freeze({ state, amplitudes, provenance });
}
