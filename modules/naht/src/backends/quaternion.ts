import type {
  NAHTState,
  TransportBackend,
  TransportStep,
} from "../types.ts";
import { validateState, validateStep } from "../core.ts";

/**
 * Unit-quaternion/SU(2) transport acting on the real three-channel vector.
 * This is a mathematical transport backend, not a claim that NAHT channels
 * are QCD color charges or a physical SU(2) gauge field.
 */
export class QuaternionSU2Backend implements TransportBackend {
  readonly id = "su2-unit-quaternion-v1";

  apply(state: NAHTState, step: TransportStep): NAHTState {
    validateState(state);
    validateStep(step);

    const [ax, ay, az] = step.rotationAxis;
    const axisNorm = Math.hypot(ax, ay, az);
    if (Math.abs(step.angleRadians) <= 1e-12 || axisNorm <= 1e-12) {
      return {
        frameId: state.frameId,
        channels: [...state.channels] as [number, number, number],
      };
    }

    const half = step.angleRadians / 2;
    const sinHalf = Math.sin(half);
    const qw = Math.cos(half);
    const qx = (ax / axisNorm) * sinHalf;
    const qy = (ay / axisNorm) * sinHalf;
    const qz = (az / axisNorm) * sinHalf;

    const [vx, vy, vz] = state.channels;
    // v' = v + 2 * q_w * (q_vec x v) + 2 * (q_vec x (q_vec x v))
    const tx = 2 * (qy * vz - qz * vy);
    const ty = 2 * (qz * vx - qx * vz);
    const tz = 2 * (qx * vy - qy * vx);

    const rx = vx + qw * tx + (qy * tz - qz * ty);
    const ry = vy + qw * ty + (qz * tx - qx * tz);
    const rz = vz + qw * tz + (qx * ty - qy * tx);

    return {
      frameId: state.frameId,
      channels: [rx, ry, rz],
    };
  }
}
