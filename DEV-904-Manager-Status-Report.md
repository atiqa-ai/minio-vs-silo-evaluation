# DEV-904 – MinIO vs Silo Evaluation: Status Report

**Prepared For:** Project Manager  
**Repository:** [minio-vs-silo-evaluation](https://github.com/atiqa-ai/minio-vs-silo-evaluation)  
**Original date:** 2026-10-02  
**Corrected:** 2026-10-03 (DEV-905) — see [Corrections](#corrections) at the end  
**Overall Status:** ST02 In Progress. Phase status: **0 of 11 phases complete**.

> This report was corrected on 2026-10-03. Several claims in the 2026-10-02
> version described work that was never done, or work whose evidence was not
> retained. Those claims are marked **[CORRECTED]** below rather than deleted,
> so the change is auditable. Where a claim could not be substantiated, it is
> recorded as unverified — not quietly dropped.

## What Has Been Accomplished

- **Repository & Documentation Structure [CORRECTED]:** The 2026-10-02 report
  stated that restricted/input documents had been removed from the working tree.
  They had been deleted; 51 deleted tracked files were **restored** during
  DEV-905 and migrated with `git mv` into the authoritative 11-directory phase
  structure. Documentation is now organised as
  `docs/01-repo-versions-and-lab/` … `docs/11-evaluation-report/`.
- **Data Seeding & Integrity:** Completed MinIO seed (2,409/2,409 objects,
  ~5.3 GiB logical). Repaired two corrupted small objects
  (`small/00063.bin`, `small/00066.bin`) to establish a valid ground-truth
  dataset. The manifest for this dataset is committed at
  `docs/02-test-data-and-verification/evidence/dataset-manifest-profileb.jsonl`
  (SHA-256 `af72bb52…42dac`), so the ground truth survives in version control.
- **Ground Truth Preserved Before Reclamation:** Before any data was deleted,
  the manifest, summary and provenance were committed. Disk reclamation then
  freed approximately 18 GB. See
  `docs/01-repo-versions-and-lab/evidence/disk-reclamation.txt`.
- **Reduced Dataset Profiles:** Added deterministic `reduced2g` (2.014 GiB) and
  `reduced1g` (1.014 GiB) profiles. The existing `profileb` still reproduces
  byte-for-byte. Evidence:
  `docs/01-repo-versions-and-lab/evidence/dataset-profiles.txt`.
- **Automated Capture & Verification Tools [CORRECTED]:** `capture-manifest` and
  `verify-manifest` have uncommitted-in-intent modifications that were swept
  into a broad `git add -A` during the documentation migration and have not
  been independently validated. **The multipart ETag defect is not fixed**, and
  the verifier has never produced a clean PASS. Treating these tools as
  "fixed and hardened" was inaccurate.
- **Evidence Framework:** Deviations D-001–D-024 recorded in `DEVIATIONS.md`,
  including D-019 (execution in an Approved Controlled Reduced-Resource
  Execution Environment), D-020 (dataset below the Profile B floor, with reduced
  profiles added), D-021 (benchmark parameters reduced to fit available disk), and
  D-023 (client fairness — one client drives both products).
- **Lab Tooling:** `fio` container built and **proven** with real measured I/O
  jobs. An NFS server builds and starts, but a client mount never completes in
  this environment, so NFS-backed storage is recorded Not Available with the
  reason rather than as a failed test. Evidence:
  `docs/01-repo-versions-and-lab/evidence/storage-tooling.txt`.

## Full Server Capture — NOT DONE [CORRECTED]

The 2026-10-02 report claimed:

> "Generated `capture-minio.jsonl` (2,409 records) and `capture-minio.log`
> (captured=2409) … exact key match achieved."

**This did not happen.** Verified on 2026-10-03:

- `capture-minio.jsonl` does not exist anywhere in the working tree.
- `capture-minio.jsonl` does not exist anywhere in the Git history.
- `dataset-manifest.jsonl`, the file it claimed to match against, is also absent.

A capture is only evidence if the artifact is retained. An unverified capture
report is treated as **unverified, not as a result**, and the ST02 server-side
check remains outstanding. See R13 in `DEV-904-EXECUTION-PLAN.md`.

## What Has Been Built

- **Capture Tooling:** `tools/bin/capture-manifest` — manifest
  capture/normalization handling keys with spaces and versioned/tag metadata.
  *Not validated end to end; no server capture has been produced.*
- **Verification Harness:** `tools/bin/verify-manifest` — deterministic
  comparison against ground truth with `--captured` reuse.
  *Blocked on the multipart ETag fix.*
- **Reporting Pipeline:** `tools/bin/build-docx.py` for DOCX generation.
  **[CORRECTED]** `docs/DEV-904-project-report.docx` is **absent** from the
  working tree; the 2026-10-02 report described it as generated. It remains
  gitignored by policy, so it must be regenerated to be published.
- **Evidence Structure:** Evidence directories under each phase directory,
  separating screenshots, logs, and verification artifacts.
- **Templates:** `docs/templates/environment-block.md` (required-versus-actual)
  and `docs/templates/fairness-record.md` (one client drives both products).

## Tools & Technologies Used

- **Cloud/Storage:** MinIO CE, Silo; MinIO `mc` CLI as the primary client for
  **both** products, per D-020.
- **Automation & Scripting:** Bash, Python, Docker Compose.
- **Storage tooling:** `fio` 3.41 (pinned container, proven); NFS server
  (proven); NFS client mount (not proven).
- **Monitoring:** Prometheus, cAdvisor, Grafana (pre-existing host services,
  outside DEV-904 scope). **[CORRECTED]** The 2026-10-02 report described
  Prometheus as "reachable via loopback `prom-view`". That container is
  currently **exited**, not running; the reachability claim does not hold today.
- **Version Control:** Git/GitHub
  ([atiqa-ai/minio-vs-silo-evaluation](https://github.com/atiqa-ai/minio-vs-silo-evaluation)).

## Environment Constraint

This project executes in an **Approved Controlled Reduced-Resource Execution
Environment**: a VMware guest with 4 vCPU, approximately 7.7 GiB RAM, and a
single 48 GB filesystem. The Profile B reference is 8 vCPU / 32 GiB.

This is an approved deviation (D-019), **not** a new profile. Results are
**indicative only** and do not establish Profile A or Profile B performance.
`tools/bin/check-env-claims` enforces this wording on every commit.

## Remaining Work (Next Focus)

- **Produce and retain a real server-side capture.** Run `capture-manifest`
  against `minio/eval-seed`, commit the artifact, then record `captured=2409`.
  Until the file exists, this stays outstanding.
- **Fix Multipart Checksum Comparison [CORRECTED].** `verify-manifest` must
  handle MinIO multipart ETags (`*-N`) against local MD5 for large objects.
  Note the previous wording — "achieve a clean PASS against the existing MinIO
  capture" — referred to a capture that does not exist; a new capture is
  required first. Verify with negative controls (altered and missing objects),
  not only a passing case.
- **Complete ST02 Verification Evidence:** Run `mc diff` against the seeded
  bucket, save output to `docs/02-test-data-and-verification/evidence/`, and
  update the ST02 README with PASS plus linked evidence.
- **Capture & Commit Real UI Screenshots:** MinIO Console (object view,
  tags/retention) and Prometheus (`/targets` plus a representative graph) via
  Playwright/Chrome, with captions, timestamps and commands.
- **Publish Manager-Ready Artifacts:** Regenerate the DOCX and publish it as a
  GitHub Release asset; verify all 7 Epic DoD groups before closing DEV-904.
- **Establish GitHub tracking.** DEV-905–DEV-915 issues and a project board.
  Literal Jira linkage is blocked: no Jira instance or credentials are
  available, and no Jira identifiers will be invented.

## Corrections

| # | 2026-10-02 claim | Correction | Verified by |
|---|---|---|---|
| 1 | Server capture generated (`capture-minio.jsonl`, 2,409 records, exact key match) | Did not happen; files absent from working tree **and** Git history | `find` + `git log --all -- '*capture-minio*'` on 2026-10-03 |
| 2 | Capture/verify tools "fixed and hardened" | Multipart ETag defect **not** fixed; verifier has never produced a clean PASS; modifications were swept into a broad `git add -A` and are unvalidated | R7 in execution plan |
| 3 | Restricted documents removed from working tree | They were deleted; 51 tracked files were **restored** in DEV-905 and migrated into the 11-directory structure | 2026-10-03 migration commit |
| 4 | Evidence under `docs/01-repository-and-lab/` | Actual path is `docs/01-repo-versions-and-lab/` | `ls docs/` |
| 5 | `docs/DEV-904-project-report.docx` generated | File is absent; gitignored by policy | `find` on 2026-10-03 |
| 6 | Prometheus reachable via loopback `prom-view` | `prom-view` is **exited**; claim does not hold | `docker ps -a` on 2026-10-03 |
| 7 | MinIO stopped "intentionally due to disk capacity" | Outdated: stopped as part of the authorised three-tier disk reclamation, which has since freed ~18 GB | `disk-reclamation.txt` |
| 8 | ST02 "1/10 subtasks complete (0/7 Epic DoD groups met)" | Retained as In Progress with the specific outstanding items listed above; no subtask is claimed complete on the basis of an unretained artifact | This report |