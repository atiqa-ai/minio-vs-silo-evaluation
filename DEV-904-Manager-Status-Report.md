# DEV-904 – MinIO vs Silo Evaluation: Status Report

**Prepared For:** Project Manager  
**Repository:** [minio-vs-silo-evaluation](https://github.com/atiqa-ai/minio-vs-silo-evaluation)  
**Date:** 2026-10-02  
**Overall Status:** ST02 in Progress – 1/10 Subtasks Complete (0/7 Epic DoD Groups Fully Met)

## What Has Been Accomplished

- **Repository & Baseline Cleanup:** Reorganized the evaluation repo, removed restricted/input documents from the working tree (with history noted), and rewrote `README.md` into a concise, manager-facing status and navigation page.
- **Data Seeding & Integrity:** Completed MinIO seed (2,409/2,409 objects, ~5.3 GiB logical). Repaired two corrupted small objects (`small/00063.bin`, `small/00066.bin`) to establish a valid ground-truth dataset.
- **Automated Capture & Verification Tools:** Fixed and hardened `tools/bin/capture-manifest` (corrected key enumeration for space-containing paths, normalized tag output) and enhanced `tools/bin/verify-manifest` (metadata normalization, added `--captured` support) to enable deterministic, reproducible verification.
- **Full Server Capture:** Generated `capture-minio.jsonl` (2,409 records) and `capture-minio.log` (captured=2409) against `minio/eval-seed` and aligned enumeration with the local `dataset-manifest.jsonl` (exact key match achieved).
- **Evidence Framework & Documentation:** Corrected audited deviations (D-016 amplification, D-017 commit prefix, D-018 tooling claims), moved objective mappings into `DEVIATIONS.md`, fixed broken/invalid references, and validated all 32 tracked Markdown files for relative links. Generated `docs/DEV-904-project-report.docx` (local build via `build-docx.py`).
- **Lab Environment Readiness:** Verified live monitoring stack (Prometheus reachable via loopback `prom-view` on `http://127.0.0.1:9090`), confirmed 4 MinIO targets `up` with `minio_*` metrics present, and documented Silo targets as **down (intentionally stopped due to disk capacity)** – not a failure condition.

## What Has Been Built

- **Capture Tooling:** Robust manifest capture/normalization pipeline (`capture-manifest`) that handles special characters, spaces, and versioned/tag metadata without corrupting keys.
- **Verification Harness:** Deterministic manifest verifier (`verify-manifest`) with captured-file reuse to avoid re-running long captures, enforcing 7-field comparison against ground truth.
- **Reporting Pipeline:** DOCX generation utility (`tools/bin/build-docx.py`) producing a structured project status report for offline/manager distribution.
- **Evidence Structure:** Organized, auditable evidence directories under `docs/01-repository-and-lab/` and `docs/02-test-data-and-verification/` with clear separation of screenshots, logs, and verification artifacts.

## Tools & Technologies Used

- **Cloud/Storage:** MinIO (single-node stack), `mc` CLI for bucket inspection/diff operations.
- **Automation & Scripting:** Bash, Python (manifest normalization, DOCX generation, verification logic).
- **Monitoring:** Prometheus + `nginx:1.27-alpine` reverse proxy (loopback-only `prom-view`), cAdvisor/Grafana (pre-existing host services, excluded from DEV-904 scope).
- **Evidence & UI Capture:** Playwright + Google Chrome (`/usr/bin/google-chrome`) for rendering/capture; Matplotlib/Python tooling for report generation.
- **Version Control & Repo:** Git/GitHub ([atiqa-ai/minio-vs-silo-evaluation](https://github.com/atiqa-ai/minio-vs-silo-evaluation)); restricted documents tracked in history only (not present in working tree).

## Remaining Work (Next Focus)

- **Fix Multipart Checksum Comparison:** Adjust `verify-manifest` to handle MinIO multipart ETags (`*-N`) vs. local MD5 for large objects (eliminate false CHECKSUM mismatches) and achieve a clean **PASS** against the existing MinIO capture.
- **Complete ST02 Verification Evidence:** Run `mc diff /dataset minio/eval-seed`, save verifier/diff outputs to `docs/02-test-data-and-verification/evidence/`, and update the ST02 README with PASS + linked evidence.
- **Capture & Commit Real UI Screenshots:** Capture MinIO Console (eval-seed object view, tags/retention) and Prometheus (`/targets` + representative graph) via Playwright/Chrome, add captions/timestamps/commands under the appropriate `screenshots/` folders, and document loopback-only access with the SSH tunnel: `ssh -L 9001:127.0.0.1:9001 -L 9090:127.0.0.1:9090 <SSH_USER>@<SERVER>`.
- **Publish Manager-Ready Artifacts:** Regenerate and make `docs/DEV-904-project-report.docx` downloadable (e.g., GitHub Release asset) since it is `.gitignore`d, commit/push all evidence and verifier changes, and **verify all 7 Epic DoD groups** are satisfied before closing DEV-904. After MinIO evidence is filed, wipe MinIO to reclaim capacity and proceed to the identical Silo turn (Silo remains intentionally stopped pending disk recovery).
