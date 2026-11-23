# Griess weight-two basis index certificate

## Result

The G0 implementation enumerates deterministic basis indices for the three
weight-two sectors used by the constructive Griess programme:

| Block | Dimension | Construction |
|---|---:|---|
| Untwisted momentum-even | 98,280 | One lexicographically canonical representative from each antipodal pair of the 196,560 norm-four Leech vectors |
| Untwisted oscillator-symmetric | 300 | Pairs \((i,j)\) with \(0\le i\le j<24\), a basis index for \(\operatorname{Sym}^2(\mathfrak h)\) |
| Twisted oscillator/ground tensor | 98,304 | Formal pairs \((g,i)\), with 0≤g<4096 and 0≤i<24 |

Consequently the untwisted fixed sector has 98,580 basis indices, the twisted
fixed sector has 98,304, and the total is 196,884.

## Reproducibility

Run:

```sh
python -m unittest tests.test_griess_weight_two_basis -v
python -m experiments.moonshine_sierpinski.griess_weight_two_basis
```

Each block receives a SHA-256 digest over its canonical ordered index data.
The momentum representatives are derived directly from the existing
Golay-based `leech_minimal_vectors()` enumerator, not from a hard-coded count.

## Interpretation boundary

This is a basis-index and dimension certificate only. The twisted ground-space
labels are formal indices; no Clifford representation or twisted module
operator action is claimed. The code does not compute any vertex-operator
modes, cocycle coefficients, intertwining operators, Griess multiplication,
invariant form, or Monster action. It is G0, not G1–G5, of
`research/GRIESS_PRODUCT_CONSTRUCTION_SPEC.md`.

The split 98,280 + 300 + 98,304 belongs to the orbifold weight-two basis.
It must not be confused with the precursor Leech VOA split
196,560 momentum + 324 oscillator states.
