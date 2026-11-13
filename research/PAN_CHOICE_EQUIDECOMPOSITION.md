# PAN Choice and Equidecomposition Research Track — v0

**Status:** isolated research module. No production wiring. No changes to PAN V8, Gosset/E8 canonical geometry, Janus Hydra, UHFE, or UDFE.

## Purpose

Explore two distinct ideas: the Axiom of Choice (AC), an existence principle for choosing from arbitrary families of nonempty sets; and Banach–Tarski, an existence theorem allowing a 3D ball to be partitioned into finitely many nonmeasurable pieces and rearranged by rigid motions into two congruent balls.

The software distinguishes finite constructive operations from nonconstructive existence claims. It does not implement arbitrary AC or construct Banach–Tarski pieces.

## Layer A — finite selection and provenance

The finite choice function selects one item from each finite nonempty family member. Default ordering by type name and representation is deterministic, not semantically privileged. Domain-specific selection should supply an explicit selector. Each decision records its method and selected representation. Candidate collections remain caller-owned and are not mutated.

The symbolic AC claim marker is existence-only, not a computable choice algorithm. The full Axiom of Choice is not generally reducible to a finite selector.

Potential later PAN interfaces include candidate Janus Hydra semantic mappings with score/provenance, compatible representation selection across modular adapters, alternative-preserving conflict resolution, and explicit distinction between chosen, rejected, and unresolved candidates.

No V8 coordinate is reinterpreted. A future adapter requires a typed contract and independent validation.

## Layer B — finite group actions and equidecomposition certificates

A finite group is represented as permutations of a finite carrier and validated for identity, closure, and inverses. The finite certificate checker verifies that source pieces are nonempty, pairwise disjoint, and cover the source; every piece is assigned exactly one group transformation and target; and moved pieces are pairwise disjoint and cover each target exactly.

This is an executable finite certificate checker. It is not a construction of Banach–Tarski. Finite permutations on a finite carrier do not reproduce the rotation-group argument on the sphere.

## Layer C — measure and theorem boundaries

Banach–Tarski relies on the Axiom of Choice in standard proofs and uses nonmeasurable subsets. Ordinary Lebesgue volume is not defined for those pieces. The theorem does not describe physical matter duplication or a laboratory process.

The measure ledger refuses a scalar measure value for objects marked nonmeasurable or unassigned.

## Relationship to PAN geometry

The module may later compare finite group actions and orbit structures on the 240-root E8 system and Gosset 4_21, finite Coxeter/Weyl group actions, and explicitly declared Janus Hydra semantic inverse pairs.

Those are finite, auditable questions. They do not establish that Banach–Tarski applies to a finite Gosset polytope, nor that mathematical equivalence implies physical equivalence.

Janus Hydra remains the semantic-geometric translator. V8 remains (h, R, u, d, tau, chi, s, f). UHFE/UDFE remain the separate coupled formation/dissolution layer.

## Validation and limitations

Run:

    python -m unittest tests.test_choice_equidecomposition -v

Tests validate finite selection, provenance recording, finite group axioms, finite partition certificates, and refusal to assign a fake measure to nonmeasurable objects. They do not prove AC, prove Banach–Tarski, construct nonmeasurable sets, or validate physical interpretations.

## Next milestone

A separate follow-up can add exact finite Weyl-group actions on the E8 root set, orbit-stabilizer checks, and equivariant mappings between the five Janus Hydra dynamic inverse pairs. Keep that work distinct from any claim about Banach–Tarski or physical measure.
