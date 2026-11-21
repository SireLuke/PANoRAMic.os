# GitHub traffic-to-development correlation audit

**Status:** proposed scheduled telemetry collector; validate repository-token access in the first workflow run.

## Purpose

Compare the repository's GitHub traffic time series with observable development events. The audit is intended to help distinguish ordinary development/CI activity from unexplained traffic bursts. It does not identify individual visitors, prove that a clone was performed by a human, or establish why a spike occurred.

## Collection

The scheduled workflow runs daily and stores a dated JSON artifact for 30 days. It requests:

- Git clone counts and unique cloners;
- page-view counts and unique visitors;
- commits created in the trailing 14-day window;
- pull requests updated in the trailing 14-day window;
- GitHub Actions workflow runs created in the trailing 14-day window.

The collector uses only the GitHub API and Python's standard library. API errors and unavailable sources are recorded in the artifact rather than silently filled with estimates.

## Access limitation

GitHub traffic endpoints are restricted to repository owners and collaborators with sufficient access. The workflow `GITHUB_TOKEN` is used for commits, pull requests, and Actions data. GitHub documents that traffic endpoints require repository Administration (read) permission for fine-grained tokens. To collect traffic, create a narrowly scoped fine-grained token with Administration: read for this repository and store it as the Actions secret `PAN_TRAFFIC_TOKEN`. The collector uses that token only for the two traffic endpoints. If the secret is absent or lacks access, the artifact records the HTTP error and still collects the other sources. Never print or commit the token.

## Reading the results

The JSON contains a `daily_correlation` table with traffic and event counts by UTC date, plus raw source responses and availability/error states.

Interpretation rules:

1. A clone is a Git operation, not a verified person. CI, agents, mirrors, repeated environments, and humans may all contribute.
2. Unique cloners are not verified unique humans.
3. Same-day coincidence is a lead for investigation, not causation. Workflows may run after a push; traffic may be delayed or aggregated.
4. Pull-request update counts are not unique reviewers or contributors.
5. The traffic endpoints expose a rolling 14-day window. Preserve daily artifacts if longer-term trend analysis is desired.
6. Compare spikes with known releases, public posts, PR merges, scheduled workflows, and external mirrors before attributing a source.

## Scope and next steps

This first implementation is intentionally read-only: it creates workflow artifacts and does not commit telemetry back to the repository, change settings, or contact visitors. After the first successful run, review API permissions and data quality, then decide whether to mirror the same collector into `SireLuke/pan-fractal-kernel` or aggregate both repositories in a separate report.

## Provenance

Generated snapshots should be treated as operational telemetry, not research validation and not evidence of external human participation.
