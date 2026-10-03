# DEV-909 — MinIO Replication

**Status: Not Started**
**Jira:** `DEV-909`
**Epic:** `DEV-904`

> **Placeholder.** This phase has not been started, so this report has no findings.
> The structure below is the template to be filled in when it runs.
>
> When it is authored, the 12 required sections must be completed in full, with the
> **expected result written before the test runs**, and every PASS backed by raw
> output in `evidence/`.

## Scope

Bucket, batch and site replication, plus the replication runbook. This phase was
folded into the former distributed-mode subtask and is now tracked separately, which
is why it has its own directory. See `DEVIATIONS.md` D-012 and the phase plan.

Gate: replication modes, failure recovery, lag and manifest verification complete.

## Controlled-environment note

Replication requires **two MinIO deployments resident at the same time** (source and
target). This is MinIO-only co-residency and is permitted; the prohibition is on
mixing MinIO and Silo nodes in one cluster, which a pre-commit hook enforces.

The dataset for this phase uses the reduced profile sized for two concurrent
deployments. The measured dataset size and the parity-2 on-disk amplification are
recorded in the environment section when the phase runs.

## Required sections

1. Goal
2. Environment
3. Prerequisites
4. Step-by-step procedure
5. Expected result
6. Actual result
7. PASS/FAIL
8. Results table
9. Findings and problems
10. Conclusion
11. How to reproduce
12. Cleanup

## Directories

| Path | Purpose |
|---|---|
| `README.md` | This document, 12 required sections |
| `evidence/` | Raw command output backing every PASS/FAIL |
| `screenshots/` | Supporting evidence only; sanitised before commit (see `../screenshots/README.md`) |
