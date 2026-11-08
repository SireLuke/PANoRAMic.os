// pillars/holdPillar.ts
//
// Shared helper for pillars that have a declared default state but no dynamics yet.
// Pure: never mutates its inputs. Throws on non-finite numbers so bad data cannot propagate silently.

export function holdPillar<T extends object>(defaults: T, current: unknown, name: string): T {
  const base = (current && typeof current === "object" ? current : {}) as Partial<T>
  const merged = { ...defaults, ...base } as T
  for (const [key, value] of Object.entries(merged)) {
    if (typeof value === "number" && !Number.isFinite(value)) {
      throw new Error(`${name} pillar: non-finite value for "${key}"`)
    }
  }
  return merged
}
