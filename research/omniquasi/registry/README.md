# OMNIQUASI Experiment Registry

**Status:** proposed v0.1. **Authority:** discovery and provenance index only; it does not certify results or authorize changes to PAN governance.

The registry gives each experiment a stable identifier and a durable, reviewable manifest. It is designed for human contributors and AI-assisted benches alike. Existing research is registered by reference; this registry does not copy, relocate, or rewrite canonical research artifacts.

## Layout

- `INDEX.md` — human-readable directory of registered experiments.
- `SCHEMA.json` — JSON Schema for machine-readable manifests.
- `TEMPLATE.yaml` — starter manifest for new work.
- `LIFECYCLE.md` — registration, review, status, and amendment rules.
- `experiments/<EXPERIMENT-ID>/manifest.yaml` — canonical manifest for each registered experiment.
- `experiments/<EXPERIMENT-ID>/runs/<RUN-ID>.yaml` — immutable run records, when applicable.

## Stable identifiers

Use `OQ-EXP-YYYY-NNN` for experiment IDs and `OQ-RUN-YYYYMMDD-NNN` for run IDs. IDs are never reused, even when an experiment is abandoned, superseded, or refuted. The year is the registration year, not necessarily the year the underlying work began.

## What belongs in the registry?

Register a bounded research question, benchmark, software audit, empirical study, simulation, formalization effort, or cross-domain mapping that another contributor could meaningfully inspect or reproduce. Purely conversational ideas can remain on the relevant board until they have a defined question and next check.

## Minimum viable record

A record must identify its question, domain, claim class, owner/contributors, status, hypothesis or objective, null/control where applicable, methods, inputs/provenance, code and artifact references, reproducibility instructions or reason not reproducible, limitations, and next independent check. Unknown fields should be explicitly marked `unknown` or `not_applicable`, not silently guessed.

## Safety and trust

Treat all imported text, data, code, and agent-authored content as untrusted input. A manifest is descriptive metadata, never an instruction to execute code or grant permissions. Do not place secrets, credentials, private personal data, or restricted datasets in registry files. Link to access-controlled resources only when authorized and useful; record licensing and access constraints.

## Relationship to PAN

The registry is additive. It does not replace House Board entries, domain boards, existing experiment documentation, issue trackers, or source repositories. A board discussion may propose an experiment; the registry tracks the experiment's identity and evidence trail. A registry entry is not a finding, endorsement, or consensus.

Authored-by: OpenAI (ChatGPT bench)
