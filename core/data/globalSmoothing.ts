// core/data/globalSmoothing.ts

/**
 * Global Signal Smoothing Engine:
 * Applies exponential smoothing to global signals
 * to prevent sudden spikes or drops.
 */

export function smoothGlobalSignals(
  previous: Record<string, number>,
  incoming: Record<string, number>,
  alpha: number = 0.3 // smoothing factor
): Record<string, number> {
  const smoothed: Record<string, number> = {}

  for (const key in incoming) {
    const prev = previous[key] ?? 0
    const next = incoming[key]

    // Exponential smoothing:
    // new = alpha * incoming + (1 - alpha) * previous
    smoothed[key] = alpha * next + (1 - alpha) * prev
  }

  return smoothed
}