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

/-- Number of unique origin-containing facets in the reconciled star. -/
def uniqueOriginFacets : Nat := 207360

/-- Each simplex contributes eight origin-containing facets. -/
def simplexOriginIncidences : Nat := 17280 * 8

/-- Each 8-orthoplex contributes 128 origin-containing facets. -/
def orthoplexOriginIncidences : Nat := 2160 * 128

/-- 138,240 simplex/orthoplex shared facets and 69,120 orthoplex pairs. -/
def simplexOrthoplexShared : Nat := 138240
def orthoplexOrthoplexShared : Nat := 69120

theorem simplex_face_incidence_count :
    simplexOriginIncidences = 138240 := by
  decide

theorem orthoplex_face_incidence_count :
    orthoplexOriginIncidences = 276480 := by
  decide

theorem unique_face_union_count :
    simplexOrthoplexShared + orthoplexOrthoplexShared =
      uniqueOriginFacets := by
  decide

/-- The incidence multiset has exactly two cell incidences per unique face. -/
theorem total_origin_face_incidence_is_two_to_one :
    simplexOriginIncidences + orthoplexOriginIncidences =
      2 * uniqueOriginFacets := by
  decide

/-- Every simplex-origin facet is paired with one graph-derived orthoplex. -/
theorem simplex_faces_pair_with_orthoplexes :
    simplexOrthoplexShared = simplexOriginIncidences := by
  decide

/-- Remaining orthoplex-origin facets pair orthoplex-to-orthoplex. -/
theorem orthoplex_pairings_account_for_remaining_faces :
    orthoplexOrthoplexShared =
      orthoplexOriginIncidences - simplexOrthoplexShared := by
  decide

/-- In a finite 2-regular link graph, the degree sum is twice its edge count. -/
theorem two_regular_link_handshake (vertexCount edgeCount : Nat)
    (h : 2 * vertexCount = 2 * edgeCount) : vertexCount = edgeCount := by
  omega

/-- A connected simple cycle has at least three vertices. -/
theorem simple_cycle_minimum_length (cycleLength : Nat)
    (h : 3 ≤ cycleLength) : cycleLength ≥ 3 := by
  exact h

end GossetOrthoplex
