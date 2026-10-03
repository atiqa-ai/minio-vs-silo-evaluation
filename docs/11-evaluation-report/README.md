# ST10 — Capability Matrix, Evaluation and Recommendation

**Status:** Not Started
**Tracker:** `DEV-915`
**Epic:** `DEV-904`
**Legacy label:** ST10

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Synthesise the evidence from ST01 through ST09 into a single capability
matrix and a recommendation, carrying every constraint forward so the conclusion
cannot be stronger than the evidence beneath it.

## Scope

In scope: the consolidated capability matrix, the recommendation with
its confidence level, the constraints and caveats that bound it, the risks of
adopting and of not adopting, and the project QA checklist.

Out of scope: new measurement. This phase runs no new tests; if a number is
needed that was not measured, it is recorded as NOT AVAILABLE rather than
estimated.

## Environment

Results were produced on a VMware guest with 4 vCPU and approximately 7.7 GiB
of RAM, below the 8 vCPU / 32 GiB reference host. They are indicative.

| Item | Value |
|---|---|
| Host | VMware guest, 4 vCPU, ~7.7 GiB RAM |
| Reference host | 8 vCPU, 32 GiB — **not met**, so all results are indicative |
| Topology | 4 nodes x 1 drive, single erasure pool, nginx load balancer |
| Images | Pinned by immutable tag and digest; recorded in ST01 |

## Prerequisites

* ST01 through ST09 complete, with raw evidence on file for every PASS relied upon.
* Every earlier phase's limitations collected, not just its results.
* Every earlier phase's deviations, host limitations and open defects collected, so none
  is silently dropped from the conclusion.
* The O01-O08 claim outcomes from ST07 available for the matrix.
* The fallback plan from ST09 available, since the recommendation must reference it.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-ST10-01` | Capability matrix | Every capability tested in any earlier phase appears in the matrix with its status and evidence path. | NOT AVAILABLE | `evidence/TC-ST10-01-<product>.txt` |
| `TC-ST10-02` | No orphan claims | Every matrix row traces to a specific evidence file; a row without evidence is removed rather than kept. | NOT AVAILABLE | `evidence/TC-ST10-02-<product>.txt` |
| `TC-ST10-03` | Constraints carried forward | Every limitation and deviation from every earlier phase appears in the conclusion, not only in its own document. | NOT AVAILABLE | `evidence/TC-ST10-03-<product>.txt` |
| `TC-ST10-04` | Recommendation stated with confidence | The recommendation names its confidence level and what would change it. | NOT AVAILABLE | `evidence/TC-ST10-04-<product>.txt` |
| `TC-ST10-05` | Both risks stated | Adopting and not adopting are each stated with their consequences. | NOT AVAILABLE | `evidence/TC-ST10-05-<product>.txt` |
| `TC-ST10-06` | Fallback plan referenced | The recommendation references the fallback plan and its stated cost. | NOT AVAILABLE | `evidence/TC-ST10-06-<product>.txt` |
| `TC-ST10-07` | Unmeasured items listed | Everything NOT AVAILABLE is listed explicitly, so absence is visible rather than implied. | NOT AVAILABLE | `evidence/TC-ST10-07-<product>.txt` |
| `TC-ST10-08` | Project QA checklist | The final checklist is completed, with each item evidenced rather than ticked. | NOT AVAILABLE | `evidence/TC-ST10-08-<product>.txt` |
| `TC-ST10-09` | Traceability | Each conclusion traces back through the phase and test case that supports it. | NOT AVAILABLE | `evidence/TC-ST10-09-<product>.txt` |

### Commands

```bash
# The matrix is built from the phases, not from memory
for f in docs/0*/README.md docs/1*/README.md; do echo "== $f"; done

# Every PASS relied upon must resolve to a file that exists
ls docs/0*/evidence/ docs/1*/evidence/

# Deviations are part of the conclusion, not an appendix
grep -n '^## D-' DEVIATIONS.md
```

### Evidence rules

* Raw command output only, one file per test case, named `TC-<id>-<product>.txt`.
* A screenshot supplements output; it never replaces it.
* Expected result is written before the run, observed result after. No back-filling.
* Every status is one of `PASS`, `FAIL`, `NOT AVAILABLE`, `NOT APPLICABLE`.

## Results

NOT AVAILABLE — phase not yet executed.

| Test case | MinIO | Silo | Notes |
|---|---|---|---|
| `TC-ST10-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST10-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST10-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST10-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST10-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST10-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST10-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST10-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST10-09` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| Capability matrix covers every capability tested, with an evidence path per row | NOT AVAILABLE | — |
| No matrix row lacks evidence | NOT AVAILABLE | — |
| Every deviation and limitation appears in the conclusion | NOT AVAILABLE | — |
| Recommendation states its confidence level and what would change it | NOT AVAILABLE | — |
| All NOT AVAILABLE items listed explicitly | NOT AVAILABLE | — |
| Project QA checklist completed with evidence per item | NOT AVAILABLE | — |
| Every conclusion traceable to a phase and test case | NOT AVAILABLE | — |

## Findings and Problems

* The host is below the reference configuration, so this evaluation cannot support a
*   production sizing recommendation. It can support a like-for-like comparison.
* The dataset failed the Profile B floor on its first iteration, realising 886 MiB against a
*   5 GB floor. Benchmarks taken from that iteration are not Profile B evidence. A later
*   iteration reached the floor; which dataset fed each number must be stated beside it.
* NFS-backed comparisons are unavailable entirely, because the client mount does not
*   complete. Those comparisons cannot be inferred from the local-storage results.
* `fio` results are a storage capability check, not a benchmark, because of the roughly 25x
*   variance between targets.
* The two products run on different Go runtimes, so Silo derives GOMAXPROCS from the cgroup
*   quota while the Go 1.24-built MinIO does not. Throughput differences are partly a
*   parallelism artefact and must not be attributed to the products alone.
* No Jira instance or credentials are available, so tracker links are greppable strings in
*   commit messages and issue bodies rather than live URLs.

## Limitations / Assumptions

**Assumptions.**
* Every status in the matrix is copied from a phase document rather than re-derived, so the matrix cannot disagree with its sources.
* Any capability not tested is absent from the matrix rather than marked as passing.
* The recommendation states what would falsify it, not only what supports it.

**Limitations.**
* The host is below the reference configuration, so this phase adds no new measurement, so every figure it reports is bound by the limitations of the phase that produced it.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. ST10 cannot be issued until every earlier phase is complete or explicitly recorded as incomplete, and every constraint has been carried into the conclusion.

## Reproduce

```bash
git clone https://github.com/atiqa-ai/minio-vs-silo-evaluation.git
cd minio-vs-silo-evaluation

cp lab/compose/.env.example lab/compose/.env   # synthetic lab credentials
./tools/bin/install-hooks                       # secret scanning
./tools/bin/lab network
```

Then follow *Procedure and Evidence*. Only one heavy cluster is started at a time.

## Cleanup

```bash
./tools/bin/lab down minio
./tools/bin/lab down silo
./tools/bin/lab down proxy
./tools/bin/lab down workload
./tools/bin/lab down storage
docker network rm migration-net
```

`lab` never passes `-v` to `docker compose down`, so cluster data in the bind
mounts under `lab/data/` survives a teardown. A dataset required by an active
evidence set is never destroyed before its evidence is captured and persisted.

## Files Changed

_To be completed when the phase runs: every file added or modified, including
evidence and any new tooling._

## Review Gate

* [ ] Requirements checked
* [ ] Expected result written before each test ran
* [ ] Evidence present for every PASS
* [ ] Failed cases retained, not deleted
* [ ] Result reproducible from the repository
* [ ] Public-repository secret scan passed
* [ ] Documentation complete
* [ ] Tracker updated
* [ ] Reviewer gate satisfied
