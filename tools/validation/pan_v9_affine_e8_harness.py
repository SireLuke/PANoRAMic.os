#!/usr/bin/env python3
"""
PAN V9 affine-E8 projection invariance harness
Read-only, standalone experiment. Does not modify a PAN repository.

Dependencies: Python 3.10+ and NumPy.
Run: python pan_v9_affine_e8_harness.py
"""
from __future__ import annotations

import itertools
import json
import math
import numpy as np

TOL = 1e-10
V8_KEYS = ("h", "R", "u", "d", "tau", "chi", "s", "f")


def build_e8_roots() -> np.ndarray:
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for si, sj in itertools.product((-1.0, 1.0), repeat=2):
            v = [0.0] * 8
            v[i], v[j] = si, sj
            roots.append(tuple(v))
    for signs in itertools.product((-1.0, 1.0), repeat=8):
        if sum(s < 0 for s in signs) % 2 == 0:
            roots.append(tuple(s / 2.0 for s in signs))
    result = np.asarray(sorted(set(roots)), dtype=float)
    assert result.shape == (240, 8)
    return result


def normalize_cloud(points: np.ndarray) -> np.ndarray:
    centered = points - points.mean(axis=0)
    rms_radius = np.sqrt(np.mean(np.sum(centered * centered, axis=1)))
    if not np.isfinite(rms_radius) or rms_radius == 0:
        raise ValueError("Cannot normalize a degenerate point cloud")
    return centered / rms_radius


# Four independent plane rotations. This is a continuous orthogonal
# display-frame family, NOT a claim that every frame is an E8 automorphism.
ROTATION_PLANES = (
    (0, 1, 1.00),
    (2, 3, 0.70),
    (4, 5, -0.40),
    (6, 7, 0.25),
)


def projection_frame(xi: float) -> np.ndarray:
    if not math.isfinite(xi):
        raise ValueError("xi must be finite")
    frame = np.eye(8)
    for i, j, rate in ROTATION_PLANES:
        angle = xi * rate
        c, s = math.cos(angle), math.sin(angle)
        frame[i, i], frame[i, j] = c, -s
        frame[j, i], frame[j, j] = s, c
    return frame


def formation_v1(v: np.ndarray) -> dict[str, float]:
    h, R, u, d, tau, chi, s, f = map(float, v)
    return {
        "bubble": (h + R + u) / 3.0,
        "honeycomb": (tau + s) / 2.0,
        "spiderweb": (f + h + R) / 3.0,
        "chiraldna": (chi + tau + R) / 3.0,
        "compoundeye": (s + h + d) / 3.0,
    }


def inverse_v1(v: np.ndarray) -> dict[str, float]:
    h, R, u, d, tau, chi, s, f = map(float, v)
    return {
        "bubble": (d + (1-u) + (1-h)) / 3.0,
        "compoundeye": ((1-s) + (1-h) + d) / 3.0,
        "honeycomb": (d + (1-tau) + (1-s)) / 3.0,
        "spiderweb": (d + (1-f) + (1-h) + (1-R)) / 4.0,
        "chiraldna": (d + (1-chi) + (1-tau) + (1-R)) / 4.0,
    }


def defect_v1(v: np.ndarray) -> dict[str, float]:
    fwd, inv = formation_v1(v), inverse_v1(v)
    return {key: fwd[key] + inv[key] - 1.0 for key in fwd}


def canonical_defect_identities(v: np.ndarray) -> dict[str, float]:
    h, R, u, d, tau, chi, s, f = map(float, v)
    return {
        "bubble": (R + d - 1.0) / 3.0,
        "compoundeye": (2.0*d - 1.0) / 3.0,
        "honeycomb": (tau + s + 2.0*d - 2.0) / 6.0,
        "spiderweb": (f + h + R + 3.0*d - 3.0) / 12.0,
        "chiraldna": (chi + tau + R + 3.0*d - 3.0) / 12.0,
    }


def main() -> None:
    roots = build_e8_roots()
    norms2 = np.sum(roots * roots, axis=1)
    assert np.allclose(norms2, 2.0, atol=TOL, rtol=0.0)

    # A root is an E8 lattice vector. Translating the entire lattice by it
    # preserves the lattice; translating this finite root cloud moves the
    # finite cloud, so only its centered/normalized shape is invariant here.
    lattice_translation = roots[0]
    z0 = normalize_cloud(roots)
    translation_error = float(np.max(np.abs(
        normalize_cloud(roots + lattice_translation) - z0
    )))
    scale_error = float(np.max(np.abs(
        normalize_cloud(3.7 * roots) - z0
    )))
    assert translation_error <= TOL
    assert scale_error <= TOL

    xis = (0.0, 0.125, 0.25, 0.5, 0.75, 1.0)
    orthogonality_error = 0.0
    determinant_error = 0.0
    roundtrip_error = 0.0
    distance_error = 0.0
    for xi in xis:
        frame = projection_frame(xi)
        orthogonality_error = max(
            orthogonality_error,
            float(np.max(np.abs(frame.T @ frame - np.eye(8))))
        )
        determinant_error = max(
            determinant_error, abs(float(np.linalg.det(frame)) - 1.0)
        )
        # Row-vector convention: transformed = source @ frame.T.
        transformed = roots @ frame.T
        restored = transformed @ frame
        roundtrip_error = max(
            roundtrip_error, float(np.max(np.abs(restored - roots)))
        )
        for k in range(1, len(roots)):
            before = np.linalg.norm(roots[0] - roots[k])
            after = np.linalg.norm(transformed[0] - transformed[k])
            distance_error = max(distance_error, abs(float(after - before)))

    assert orthogonality_error <= TOL
    assert determinant_error <= TOL
    assert roundtrip_error <= TOL
    assert distance_error <= TOL
    assert np.allclose(projection_frame(0.0), np.eye(8), atol=TOL, rtol=0.0)

    # A 2D view is intentionally lossy. Keep canonical source points and
    # indices separately; never claim that the 2D coordinates invert to R^8.
    xi_view = 0.5
    rotated = roots @ projection_frame(xi_view).T
    p2 = np.eye(8)[:2, :]
    displayed = rotated @ p2.T
    reconstructed = displayed @ p2 @ projection_frame(xi_view)
    residuals = np.linalg.norm(roots - reconstructed, axis=1)
    max_2d_residual = float(np.max(residuals))
    assert max_2d_residual > TOL

    # V8 is an independent semantic payload. Geometry view operations do not
    # transform it. This is a pass-through contract, not a geometry-to-V8 map.
    v8 = np.array([0.8, 0.7, 0.75, 0.25, 0.65, 0.6, 0.72, 0.55])
    assert v8.shape == (8,) and np.all((v8 >= 0.0) & (v8 <= 1.0))
    baseline_f = formation_v1(v8)
    baseline_i = inverse_v1(v8)
    baseline_d = defect_v1(v8)
    identity_values = canonical_defect_identities(v8)
    identity_error = max(
        abs(baseline_d[key] - identity_values[key])
        for key in baseline_d
    )
    assert identity_error <= TOL
    for xi in xis:
        _display_frame = projection_frame(xi)
        assert formation_v1(v8) == baseline_f
        assert inverse_v1(v8) == baseline_i
        assert defect_v1(v8) == baseline_d

    # The checked-in repository implementation must be audited separately:
    # this standalone harness implements the requested canonical v1 equations
    # and does not silently certify the current repository's older code.
    result = {
        "harness": "PAN V9 affine-E8 projection invariance",
        "classification": "independent equation/numerical harness; not repository pytest",
        "root_count": int(len(roots)),
        "root_norm_squared": {
            "min": float(np.min(norms2)),
            "max": float(np.max(norms2)),
        },
        "translation_normalized_cloud_max_error": translation_error,
        "positive_scale_normalized_cloud_max_error": scale_error,
        "projection_xi_samples": list(xis),
        "projection_frame_max_orthogonality_error": orthogonality_error,
        "projection_frame_max_determinant_error": determinant_error,
        "8d_forward_reverse_max_error": roundtrip_error,
        "pairwise_distance_max_error": distance_error,
        "neutral_xi_is_identity": bool(np.array_equal(projection_frame(0.0), np.eye(8))),
        "2d_view_max_reconstruction_residual": max_2d_residual,
        "2d_view_is_lossless": bool(max_2d_residual <= TOL),
        "canonical_v1_defect_identity_max_error": identity_error,
        "canonical_v1_scores_defects_xi_independent": True,
        "v8_coordinate_order": list(V8_KEYS),
        "repository_files_modified": False,
        "limitations": [
            "Continuous orthogonal display frames are not generally E8 lattice automorphisms.",
            "A translated finite root set is not itself the original 240-root set; the full E8 lattice is translation-invariant under lattice vectors.",
            "A dimension-reducing view is lossy; source coordinates and root identities must be retained.",
            "No physical interpretation, SU(9) coupling, or 9D Navier-Stokes claim is tested.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
