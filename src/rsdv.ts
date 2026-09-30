import type { AuditResult } from "./rams.ts";

export function computeRSDV(audit: AuditResult): number {
  // Simple weighted placeholder; later you can refine the model.
  const factors = [
    1 - audit.waterScarcity,
    audit.foodStability,
    audit.energyAvailability,
    audit.biomeHealth,
    1 - audit.climateVolatility,
    1 - audit.extractionPressure,
    audit.recyclingThroughput,
  ];

  const avg = factors.reduce((a, b) => a + b, 0) / factors.length;
  const rsdv = 0.65 + (avg * (1.0 - 0.65)); // clamp between 0.65–1.0

  return Math.min(1.0, Math.max(0.65, rsdv));
}
