import Mathlib

namespace GossetOrthoplex

/-- Number of antipodal pairs in a regular 2k-vertex orthoplex facet. -/
def oppositePairCount (k : Nat) : Nat := k

/-- Cross-pairs between distinct antipodal pairs: four per pair of pairs. -/
def crossPairCount (k : Nat) : Nat := 4 * Nat.choose k 2

theorem seven_pairs_have_fourteen_vertices :
    2 * oppositePairCount 7 = 14 := by
  norm_num [oppositePairCount]

theorem seven_pair_cross_edges :
    crossPairCount 7 = 84 := by
  norm_num [crossPairCount]

theorem seven_pair_non_edges :
    oppositePairCount 7 = 7 := by
  rfl

theorem k14_minus_matching_edge_count :
    Nat.choose 14 2 - oppositePairCount 7 = crossPairCount 7 := by
  norm_num [oppositePairCount, crossPairCount]

end GossetOrthoplex
