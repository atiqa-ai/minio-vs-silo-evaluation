# DEV-904 – Daily Task Report: 03 October 2026

**Prepared For:** Project Manager
**Prepared By:** Atiqa Ahmed
**Repository:** [minio-vs-silo-evaluation](https://github.com/atiqa-ai/minio-vs-silo-evaluation)
**Report Date:** 2026-10-03 (Saturday)
**Phase Focus:** DEV-905 (Repository, Versions & Lab) and DEV-906 (Test Data & Verification)
**Overall Status:** **0 of 11 phases complete.** Planning complete; execution not started.

---

## 1. Executive Summary

Today's work removed the gaps that stood between this project and being executable.
Twenty-five commits of engineering work were pushed across 105 files
(+7,145 / −632 lines); this report is the twenty-sixth commit.

The single most consequential finding is that **DEV-909 could not have been run at
all** — its documented commands referenced a Compose project that did not exist in
the repository. That project now exists and is verified.

A second theme was documentation integrity. Ninety-six unresolvable specification
citations were replaced with the actual rule text, and the same fabricated citations
were subsequently found in the code and configuration, including roughly a dozen
comments that attributed the lab's port policy to a specification section that does
not exist. **The specification says nothing about ports anywhere.** The lab's port
policy is now recorded as a lab decision rather than as a requirement.

No phase was executed and none was signed off. That is deliberate: this report
records a verified, reproducible foundation, not results.

---

## 2. Work Completed

### 2.1 Documentation & Planning

| # | Task | Outcome |
|---|---|---|
| 1 | Replaced 96 unresolvable specification citations | Real rule text substituted; zero invalid citations remain repo-wide |
| 2 | Wrote complete pre-test plans for 9 previously stub phases | 11/11 phases now contain all 14 required sections in order |
| 3 | Specified test cases for every phase | **175 test cases** with expected results, so no phase needs further design |
| 4 | Added the 5 template sections missing from DEV-905 / DEV-906 | Structural compliance restored without renumbering existing references |
| 5 | Repaired broken cross-references | 25/25 relative links resolve; all phase references verified |
| 6 | Rewrote the root README to actual project state | Removed 2 false claims; documented the true position |

### 2.2 Laboratory & Tooling

| # | Task | Outcome |
|---|---|---|
| 7 | **Built the missing replication target** | `lab/compose/replication-target/` — 4-node MinIO (`rep-minio-1..4`), own credentials, no published ports. DEV-909 is now executable |
| 8 | Extended manifest tooling to accept `rep` | `capture-manifest` and `verify-manifest` previously accepted only `minio\|silo`, so the target's manifest could not be verified at all |
| 9 | Enforced the two-deployment exception in code | `lab up rep-target` refuses to run while Silo is up; tested both directions |
| 10 | Made the mixed-cluster check self-discovering | It previously listed its input files, so a new cluster escaped by not being named |
| 11 | Built containerised storage tooling | `fio-local:3.41-r0` and `nfs-local:2.6.4-r6`, wired into `lab/compose/storage/` |
| 12 | Added reduced dataset profiles | `reduced2g` (2.014 GiB) and `reduced1g` (1.014 GiB); `profileb` still byte-identical |
| 13 | Pinned `mcli` from the product image | Recorded as D-023; no unpinned binary enters the project |
| 14 | Reclaimed disk under recorded authorisation | ~18 GB freed, with before/after evidence |

### 2.3 Governance & Tracker

| # | Task | Outcome |
|---|---|---|
| 15 | Repaired all 12 GitHub issue bodies | Removed unsupported completion claims |
| 16 | Enforced environment terminology via pre-commit hook | Blocks invented profile names and unsupported compliance claims |
| 17 | Scanned full history for secrets | 30 commits, **0 leaks** |
| 18 | Verified local and remote are identical | All **105 tracked blobs** matched by hash from a fresh clone |

---

## 3. Defects Found and Fixed

1. **Replication target absent.** DEV-909's documented commands referenced
   `lab/compose/replication-target/compose.yml`, which did not exist. The phase
   was unrunnable as written.
2. **Negative control compared the target against itself.** The verification
   command passed the capture in the manifest position, so every object would
   match and the check would report success on a deliberately tampered bucket —
   a guaranteed false pass on the exact test meant to catch tampering.
3. **Mixed-cluster check had a hardcoded file list.** A newly added cluster was
   invisible to it, which is how the replication target initially escaped review.
4. **Environment misrepresented.** The README described the host as an "approved
   controlled reduced-resource environment". D-004 records that the requirements
   *prohibit* virtualisation; D-019 records a decision to proceed anyway. These are
   different things — one is a choice, the other a property of the measurement —
   and conflating them invites the reader to believe the reference configuration
   was met. It was not.
5. **Fabricated specification citations in code.** Compose files, Dockerfiles and
   11 scripts cited guardrails and SRD sections that do not exist.
6. **Two deviations mislabelled.** The manager status report described D-020 as
   "client fairness" and D-021 as "reduced dataset". D-020 is the dataset being
   below the Profile B floor; D-021 is benchmark parameters reduced to fit disk;
   client fairness is D-023. Corrected in this commit.

---

## 4. Risks, Blockers and Open Items

| Item | Impact | Status |
|---|---|---|
| **NFS client mount** | DEV-910 and DEV-913 NFS-backed comparisons cannot run | **Blocked.** Server side proven (export, `rpc.nfsd`, NFSv4 on 2049 — after fixing a real defect where `rpcbind` wedged registration). Client side fails: v4 hangs with and without `nolock`; v3 fails on `rpc.statd`, then `Not supported` |
| **R7 — multipart ETag vs local MD5** | Multipart objects cannot verify | **Open.** Negative control still required |
| **R13 — no server-side capture** | Dataset integrity not independently proven | **Open** |
| **fio variance** | Back-to-back runs differed ~20% | Reported as **capability-only**; fio may only show the tool runs |
| **GitHub Project board** | Cannot update the board | Blocked — requires `read:project` scope |
| **Deviations D-010 / D-018 stale** | Register contradicts the repository | Open — both describe the `fio`/NFS tooling as unbuilt; it now exists |

Nothing above is recorded as a test failure. Where a check cannot run, the status is
**Not Available**, which is deliberately distinct from *Failed*.

---

## 5. Project Status

| Metric | Value |
|---|---|
| Phases with a complete pre-test plan | **11 of 11** |
| Phases executed and signed off | **0 of 11** |
| Test cases specified | **175** |
| Phases with raw evidence captured | 2 (DEV-905, DEV-906) |
| Subtasks closed | **0 of 11** |
| Epic DoD groups fully met | **0 of 7** |
| Open defects | 3 (R7, R13, NFS client mount) |

**The plan is finished; the run has not started.** The gap between those two facts is
the entire remaining workload, and it is measurement rather than design.

---

## 6. Next Working Day — Planned Actions

1. Resolve **R7** and execute its negative control, so multipart objects verify or
   provably cannot.
2. Generate and commit the **R13** server-side capture to close the dataset-integrity gap.
3. Begin execution of **DEV-907**, the first phase with zero evidence.
4. Update **D-010 / D-018** in the deviations register to reflect the built tooling.
5. Confirm NFS client feasibility, or formally record DEV-910/DEV-913 NFS cases as
   Not Available with the measured reason.

---

## 7. Carry-Forward State

Work continues from commit `55ab3c5` on `main`. The following are true and require no
re-derivation:

- Local and remote trees are byte-identical (105/105 tracked blobs verified by hash).
- All 7 Compose projects validate; all 3 pre-commit hooks pass on a clean clone.
- All 11 phase documents are structurally complete and unexecuted.
- Ground-truth dataset manifest is committed at
  `docs/02-test-data-and-verification/evidence/dataset-manifest-profileb.jsonl`
  (SHA-256 `af72bb52…42dac`).
- Captured evidence files are unmodified; later corrections are appended as dated
  notes so the original capture stays auditable.

---

*All work committed and pushed. Full-history secret scan clean. Verification evidence
for every claim above is under each `docs/<phase>/evidence/` directory.*