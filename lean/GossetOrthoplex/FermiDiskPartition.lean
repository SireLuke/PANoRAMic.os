import Lean

namespace GossetOrthoplex

/-- Signed occupancy contrast delta = 2N - 1. -/
def occupancyDelta (n : Rat) : Rat := 2 * n - 1

/-- White area fraction for the two-semicircle unit-disk partition. -/
def whiteDiskAreaFraction (n : Rat) : Rat :=
  (1 : Rat) / 2
    - (1 - occupancyDelta n) ^ 2 / 8
    + (1 + occupancyDelta n) ^ 2 / 8

/-- Black area is the complementary region of the unit disk. -/
def blackDiskAreaFraction (n : Rat) : Rat :=
  1 - whiteDiskAreaFraction n

/-- The five displayed white occupancy states are exact area fractions. -/
theorem white_area_at_95_percent :
    whiteDiskAreaFraction (95 / 100) = 95 / 100 := by decide

theorem white_area_at_75_percent :
    whiteDiskAreaFraction (75 / 100) = 75 / 100 := by decide

theorem white_area_at_50_percent :
    whiteDiskAreaFraction (50 / 100) = 50 / 100 := by decide

theorem white_area_at_25_percent :
    whiteDiskAreaFraction (25 / 100) = 25 / 100 := by decide

theorem white_area_at_5_percent :
    whiteDiskAreaFraction (5 / 100) = 5 / 100 := by decide

/-- The black complementary fractions are exact at the same five states. -/
theorem black_area_at_95_percent :
    blackDiskAreaFraction (95 / 100) = 5 / 100 := by decide

theorem black_area_at_75_percent :
    blackDiskAreaFraction (75 / 100) = 25 / 100 := by decide

theorem black_area_at_50_percent :
    blackDiskAreaFraction (50 / 100) = 50 / 100 := by decide

theorem black_area_at_25_percent :
    blackDiskAreaFraction (25 / 100) = 75 / 100 := by decide

theorem black_area_at_5_percent :
    blackDiskAreaFraction (5 / 100) = 95 / 100 := by decide

end GossetOrthoplex
