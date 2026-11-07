export interface GovernanceDecision {
  readonly decisionId: string;
  readonly policyId: string;
  readonly policyVersion: string;
  readonly scope: string;
  readonly rationale: string;
  readonly evidenceRefs: readonly string[];
  readonly proposerId: string;
  readonly authorizerId: string;
  readonly implementerId: string;
  readonly verifierId: string;
  readonly conflictsDeclared: boolean;
  readonly authorizationBasis: string;
  readonly proposedAt: string;
  readonly authorizedAt: string;
  readonly effectiveAt: string;
  readonly reviewAt: string;
  readonly privacyClass: "public" | "restricted" | "sensitive";
}

export interface GovernanceDecisionValidation {
  readonly valid: boolean;
  readonly errors: readonly string[];
}

/**
 * Validates record completeness and minimum separation-of-duties rules.
 * This is a structural guard, not a vote, legal determination, or proof that
 * an authorizing body actually had authority.
 */
export function validateGovernanceDecision(
  decision: GovernanceDecision,
): GovernanceDecisionValidation {
  const errors: string[] = [];
  const required: (keyof GovernanceDecision)[] = [
    "decisionId", "policyId", "policyVersion", "scope", "rationale",
    "proposerId", "authorizerId", "implementerId", "verifierId",
    "authorizationBasis", "proposedAt", "authorizedAt", "effectiveAt",
    "reviewAt",
  ];

  for (const key of required) {
    const value = decision?.[key];
    if (typeof value !== "string" || value.trim().length === 0) {
      errors.push(`${key} is required`);
    }
  }

  if (decision && decision.proposerId === decision.authorizerId) {
    errors.push("Proposer and authorizer must be separate roles");
  }
  if (decision && decision.implementerId === decision.verifierId) {
    errors.push("Implementer and verifier must be separate roles");
  }
  if (decision && decision.conflictsDeclared !== true) {
    errors.push("Conflict-of-interest declaration must be explicitly recorded");
  }
  if (decision && !Array.isArray(decision.evidenceRefs)) {
    errors.push("evidenceRefs must be an array");
  }

  if (decision) {
    const dates = ["proposedAt", "authorizedAt", "effectiveAt", "reviewAt"] as const;
    const parsed: Partial<Record<typeof dates[number], number>> = {};
    for (const key of dates) {
      const value = Date.parse(decision[key]);
      if (!Number.isFinite(value)) errors.push(`${key} must be a valid date-time`);
      else parsed[key] = value;
    }
    if (parsed.effectiveAt !== undefined && parsed.reviewAt !== undefined &&
        parsed.reviewAt <= parsed.effectiveAt) {
      errors.push("reviewAt must be later than effectiveAt");
    }
    if (parsed.proposedAt !== undefined && parsed.authorizedAt !== undefined &&
        parsed.authorizedAt < parsed.proposedAt) {
      errors.push("authorizedAt cannot precede proposedAt");
    }
  }

  return Object.freeze({ valid: errors.length === 0, errors: Object.freeze(errors) });
}
