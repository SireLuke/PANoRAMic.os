# PAN / NAHT Licensing and Contributor Policy

**Identifier:** PAN-LIC-001  
**Status:** Proposed policy; not a final license notice

## 1. Release direction

PAN and NAHT are pursuing a copyleft-first release strategy. GNU AGPL-3.0 is the leading candidate for NAHT Core and potentially compatible PAN components, but no repository-wide license change is made by this document.

Before selecting a license for any repository or component:
- inventory existing copyright notices and authorship;
- inventory dependencies and transitive licenses;
- identify files with unclear ownership;
- check whether the proposed license is compatible with the component's dependencies and distribution model;
- document the exact license version and scope;
- preserve third-party notices and attribution.

Do not add an AGPL header or claim that the repository is AGPL-licensed until the project has made and recorded that decision.

## 2. Component-level licensing

The repository contains existing components with potentially different histories and dependencies. Licensing must be reviewed at the component/repository boundary; a new module's package metadata does not automatically relicense existing files.

NAHT Core is designed to be a separable package. Its eventual license should be explicit in the published package, source distribution, and repository notices. PAN adapters may have additional dependencies and must be reviewed independently for compatibility.

## 3. Contributor provenance

The initial contribution process should use a Developer Certificate of Origin (DCO)-style sign-off, subject to project adoption.

Contributors should confirm:
- they authored the contribution or have authority to submit it;
- they have identified known third-party code and applicable license terms;
- they are not knowingly submitting confidential or improperly obtained material;
- they have disclosed known patent or contractual restrictions relevant to the contribution.

Keep authorship attribution and contribution history. Do not require copyright assignment under this policy.


### DCO sign-off and AI-assisted work

If the project adopts a DCO, the sign-off is a personal certification by the identified human signatory under the exact adopted text. An AI system or model must not be named as the `Signed-off-by` signatory. A human submitter, relayer, maintainer, or committer must not sign merely because they handled the Git operation: they must personally have the rights and authority required by the adopted DCO and be able to truthfully make each certification it contains. If that is uncertain, hold the contribution for clarification rather than adding a ceremonial or proxy sign-off.

Substantive AI assistance should be credited separately in the pull request or contribution record (for example, `AI contribution: ChatGPT bench (OpenAI), model/version when known`), with the contributed work and the human relayer/filer identified where applicable. This descriptive provenance is not a DCO certification, does not make the AI system a legal author or signatory, and does not imply provider endorsement. Git author, committer, DCO signatory, reviewer, relayer, and filer are distinct roles and must not be conflated.

This policy remains proposed. Before requiring sign-off, the project must select and publish the exact DCO text and document how it applies to AI-assisted contributions. This section is governance guidance, not legal advice; unresolved rights or certification questions should be escalated rather than guessed.

## 4. Patent terms

The selected copyleft license may include contributor patent grants and termination conditions. Explain those terms to contributors before adoption. Any patent strategy must be consistent with the exact license text and contributor commitments.

This policy does not promise dual licensing. Dual licensing requires a separate rights strategy and appropriate permissions from all relevant rightsholders.

## 5. Ethical use and open-source distinction

NAHT-SAFE-001 governs official project conduct, certified deployments, and project-controlled services. It is separate from the open-source license.

Do not insert purpose-of-use restrictions into an OSI-compliant license and then describe the result as OSI-compliant open source. Third-party forks may remove project governance safeguards; the project must not claim control over them.

## 6. Release checklist

- [ ] Ownership and provenance inventory complete.
- [ ] Dependency/license inventory complete.
- [ ] License choice and version recorded.
- [ ] Required notices included.
- [ ] Contributor sign-off process documented.
- [ ] Patent review completed for disclosure-sensitive material.
- [ ] Safety/certification terms kept separate from license permissions.
