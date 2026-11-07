# PAN / NAHT Patent Review Gate

**Identifier:** PAN-IP-001  
**Status:** Internal project procedure; not legal advice

## 1. Objective

Avoid accidental public disclosure of a specific technical implementation that the project may wish to evaluate for patent protection. The project does not assume that any particular idea or implementation is patentable.

## 2. Review triggers

A contributor or maintainer may open an invention review when a specific implemented mechanism appears to solve a technical problem in a potentially novel way.

Candidate areas may include:
- concrete ordered history-transport implementations;
- specific junction processing or topology/transport coordination;
- reproducible provenance and deterministic replay mechanisms;
- specific host-isolation or permission-boundary mechanisms.

Broad ideas, abstract goals, mathematical concepts, or desired outcomes alone are not presumed patentable.

## 3. Invention record

Record:
- title, contributors, and responsible maintainer;
- problem statement and concrete implementation;
- diagrams, pseudocode, source references, and experimental evidence;
- what is believed to differ from known approaches;
- known prior art and competing implementations;
- dates of conception, implementation, demonstration, offer, and disclosure;
- third-party code, contracts, and ownership concerns;
- decision and decision date.

Keep sensitive details in a restricted location. Do not place confidential invention details in public issue trackers.

## 4. Disclosure hold

While an item is marked `PATENT_REVIEW_PENDING`, do not publish the disclosure-sensitive implementation details in a public repository, paper, talk, demo, or public discussion until the project records a release decision.

The hold must be scoped to the specific material; it must not be used to suppress unrelated open development or contributors' independent work.

## 5. Decision options

- **File review:** seek qualified patent advice and decide whether and where to file.
- **Defensive publication:** deliberately publish enough detail to establish prior art, after confirming this is the intended strategy.
- **Open release:** publish without pursuing patent protection.
- **Confidential retention:** retain as a trade secret only where lawful, operationally feasible, and consistent with project commitments.
- **No action:** close the review with a recorded rationale.

## 6. License coordination

Before adopting AGPL-3.0, review its contributor patent grant and termination terms. Patent ownership, contributor grants, and license promises must not conflict.

## 7. Practical low-cost process

The project can maintain an invention log, perform preliminary public prior-art searches, and use public USPTO resources to understand filing processes. These activities are not a substitute for legal advice on eligibility, claim drafting, ownership, disclosure deadlines, or foreign filing strategy.

No provisional filing is assumed to protect all later claims. No universal grace period is assumed. Jurisdiction-specific consequences must be checked before disclosure.

## 8. Required release decision

Every release candidate must record whether any active patent-review holds affect the proposed release. The release record must identify cleared, excluded, or deferred materials without exposing confidential details.
