# NAHT-SAFE-001 — Responsible Use and Deployment Covenant

**Status:** Proposed project covenant  
**Applies to:** Official NAHT project, maintainers, project-controlled services, and certified deployments

## 1. Commitment

The official NAHT project and certified deployments must not knowingly design, authorize, or facilitate uses intended to cause malicious harm, violence, exploitation, coercion, unlawful surveillance, or deliberate abuse.

## 2. Scope

This covenant governs project stewardship, certification, and project-controlled services. It does not claim to control every third-party fork or independently operated deployment.

## 3. Capability separation

Deployments should distinguish:
- read;
- analyze;
- simulate;
- export;
- configure;
- execute or actuate.

Higher-impact capabilities must not be inherited automatically from read or analysis access. Host execution requires explicit host authorization and human approval proportionate to impact.

## 4. Safeguards

Certified deployments should implement:
- purpose and risk assessment;
- least-privilege permissions and default-deny extensions;
- human oversight proportionate to impact;
- tamper-evident records for consequential actions;
- reproducible configuration and version provenance;
- incident reporting, restriction, suspension, and revocation procedures;
- independent review for high-impact deployments.

## 5. Misuse response

On credible evidence of misuse or compromise, the responsible operator should preserve evidence, restrict affected credentials or extensions, suspend certification where justified, notify affected parties where appropriate, and document remediation and reinstatement conditions.

Emergency restrictions must be narrowly scoped, logged, time-limited, and reviewable.

## 6. License boundary

This covenant is separate from AGPL-3.0. It must not be misrepresented as a purpose-of-use restriction contained in an OSI-compliant open-source license. Its enforceability depends on applicable contracts, certification terms, deployment control, and law.

## 7. Limitations

No technical safeguard guarantees that all downstream uses will be safe. Forks may remove safeguards. Certification is a bounded conformance assessment, not a guarantee of legal compliance or harmlessness.
