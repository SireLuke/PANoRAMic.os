// engine/par/parDignityEngine.ts

export function computeParDignity({
  par,
  salaries,
  markets,
  ecology,
  infrastructure,
}: {
  par: any
  salaries: any
  markets: any
  ecology: any
  infrastructure: any
}) {
  // Base dignity from floor + float
  let dignityScore =
    salaries.dignityFloor * 0.4 +
    par.dignityFloat * 0.6

  // Ecology and infrastructure support dignity
  dignityScore += ecology.regenerationIndex * 20
  dignityScore += infrastructure.resilienceIndex * 20

  // Extraction pressure harms dignity
  dignityScore -= markets.extractivePressureIndex * 30

  // Ensure dignity floor is respected
  const dignityCompliant = dignityScore >= salaries.dignityFloor

  // Recovery: if dignity is low, slowly raise floor
  if (!dignityCompliant) {
    salaries.dignityFloor += 5
  }

  // Bound dignity score
  dignityScore = Math.max(0, dignityScore)

  return {
    dignityScore,
    dignityCompliant,
    updatedDignityFloor: salaries.dignityFloor,
  }
}
