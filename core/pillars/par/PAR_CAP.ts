export function computeParCap({
  population,
  dignityFloat,
  resourceModifier,
  marketBurden,
  ecologyRegen,
  infrastructureResilience,
}) {
  return (
    population *
    dignityFloat *
    resourceModifier *
    (1 - marketBurden) *
    ((ecologyRegen + infrastructureResilience) / 2)
  )
}
