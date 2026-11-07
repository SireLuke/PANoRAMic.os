import {
  validateGovernanceDecision,
  type GovernanceDecision,
} from "../../governance/core/decision.ts";

const validDecision: GovernanceDecision = {
  decisionId: "decision-001",
  policyId: "policy-001",
  policyVersion: "1.0.0",
  scope: "test deployment",
  rationale: "Exercise the decision-record contract",
  evidenceRefs: ["audit://evidence/001"],
  proposerId: "community-member-1",
  authorizerId: "council-1",
  implementerId: "operator-1",
  verifierId: "auditor-1",
  conflictsDeclared: true,
  authorizationBasis: "Recorded council authorization",
  proposedAt: "2026-11-06T12:00:00Z",
  authorizedAt: "2026-11-06T13:00:00Z",
  effectiveAt: "2026-11-07T00:00:00Z",
  reviewAt: "2026-12-07T00:00:00Z",
  privacyClass: "public",
};

const valid = validateGovernanceDecision(validDecision);
if (!valid.valid) throw new Error(valid.errors.join("; "));

const invalid = validateGovernanceDecision({
  ...validDecision,
  verifierId: validDecision.implementerId,
});
if (invalid.valid) throw new Error("Implementer/verifier role collision was not rejected");

console.log("PAN governance checks passed.");
