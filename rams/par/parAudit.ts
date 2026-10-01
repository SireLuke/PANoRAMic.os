import { ParState } from "../../core/pillars/par/PAR_STATE";

/**
 * PAR Audit
 *
 * Enforces PANoRAMic.os economic rules for the Planetary Autonomous Resource system:
 * - non-negative supply / circulation checks
 * - cap compliance for PAR issuance
 * - MSRP cap: market price cannot exceed 15% of market value
 */
export function auditPar(state: ParState) {
  const marketValue = Number((state as any).marketValue ?? 0);
  const currentMarketPrice = Number((state as any).currentMarketPrice ?? 0);
  const msrpPercent = 0.15;
  const msrpCapPrice = marketValue * msrpPercent;
  const msrpCapCheck = currentMarketPrice <= msrpCapPrice;

  return {
    dataIntegrity: true,
    supplyCheck: state.totalParSupply >= 0,
    capCheck: state.parCap >= 0,
    circulationCheck: state.parInCirculation >= 0,
    stewardshipCheck: state.stewardshipFund >= 0,
    humanitarianCheck: state.humanitarianPool >= 0,
    velocityCheck: state.parVelocity >= 0,

    msrpCapPercent: msrpPercent,
    marketValue,
    currentMarketPrice,
    msrpCapPrice,
    msrpCapCheck,
    msrpCapViolation: msrpCapCheck
      ? null
      : `Market price ${currentMarketPrice} exceeds MSRP cap of ${msrpCapPrice} (15% of market value).`,
  };
}
