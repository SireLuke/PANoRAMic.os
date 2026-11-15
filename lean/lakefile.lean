import Lake
open Lake DSL

package «gosset-orthoplex-audit» where
  -- Isolated research formalization; no production dependency.

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

lean_lib GossetOrthoplex
