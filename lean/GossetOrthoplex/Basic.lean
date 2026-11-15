import Lean

namespace GossetOrthoplex

/-- Number of antipodal pairs in a regular 2k-vertex orthoplex facet. -/
def oppositePairCount (k : Nat) : Nat := k

/-- Cross-pairs between distinct antipodal pairs: four per pair of pairs. -/
def crossPairCount (k : Nat) : Nat := 4 * Nat.choose k 2

theorem seven_pairs_have_fourteen_vertices :
    2 * oppositePairCount 7 = 14 := by
  decide

theorem seven_pair_cross_edges :
    crossPairCount 7 = 84 := by
  decide

theorem seven_pair_non_edges :
    oppositePairCount 7 = 7 := by
  decide

/-- K14 has 91 unordered pairs; removing the seven opposite pairs leaves 84. -/
theorem k14_minus_matching_edge_count :
    Nat.choose 14 2 - oppositePairCount 7 = crossPairCount 7 := by
  decide

end GossetOrthoplex
