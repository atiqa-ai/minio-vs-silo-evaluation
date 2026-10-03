# ST08 — Silo Benchmark

**Status:** Not Started
**Tracker:** `DEV-913`
**Epic:** `DEV-904`
**Legacy label:** ST08

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Measure Silo with the identical method, parameters and dataset used in ST04,
so the two performance results are genuinely comparable.

ST04 declared its parameters in advance. This phase must reuse them unchanged.
Choosing parameters again here would make any difference uninterpretable.

## Scope

In scope: the same small-object, large-object, mixed, multipart,
versioned, topology, storage, repetition, noisy-neighbour and resource-limit
cases as ST04, executed against the Silo cluster.

Out of scope: MinIO-side measurement (ST04, [`docs/06-minio-performance-baseline`](../06-minio-performance-baseline/README.md)), functional behaviour
(ST03, ST06), compatibility (ST07), and the recommendation (ST10).

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

* ST04 complete, with its declared parameters, repetitions and raw output on file.
* **The ST04 parameter set is reused unchanged.** A parameter changed between ST04 and ST08 invalidates the comparison.
* The same Profile B dataset bytes as ST04, regenerated rather than copied.
* MinIO fully stopped before Silo starts; only one heavy cluster runs at a time.
* `silo-client` and `mcli` available; the workload is driven the same way it was for MinIO.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-ST08-01` | Raw disk on the Silo storage path | `fio` on the Silo data directories, measured and reported with the same variance caveat as ST04. | NOT AVAILABLE | `evidence/TC-ST08-01-<product>.txt` |
| `TC-ST08-02` | Small-object PUT | Identical object size, count and duration to TC-ST04-03. | NOT AVAILABLE | `evidence/TC-ST08-02-<product>.txt` |
| `TC-ST08-03` | Small-object GET | Identical parameters to TC-ST04-04. | NOT AVAILABLE | `evidence/TC-ST08-03-<product>.txt` |
| `TC-ST08-04` | Small-object DELETE | Identical parameters to TC-ST04-05. | NOT AVAILABLE | `evidence/TC-ST08-04-<product>.txt` |
| `TC-ST08-05` | Object LIST | Identical parameters to TC-ST04-06. | NOT AVAILABLE | `evidence/TC-ST08-05-<product>.txt` |
| `TC-ST08-06` | Large-object PUT | Identical parameters to TC-ST04-07. | NOT AVAILABLE | `evidence/TC-ST08-06-<product>.txt` |
| `TC-ST08-07` | Large-object GET | Identical parameters to TC-ST04-08. | NOT AVAILABLE | `evidence/TC-ST08-07-<product>.txt` |
| `TC-ST08-08` | Mixed workload | Identical mix ratio to TC-ST04-09. | NOT AVAILABLE | `evidence/TC-ST08-08-<product>.txt` |
| `TC-ST08-09` | Multipart upload | Identical part size and count to TC-ST04-10. | NOT AVAILABLE | `evidence/TC-ST08-09-<product>.txt` |
| `TC-ST08-10` | Versioned workload | Identical parameters to TC-ST04-11. | NOT AVAILABLE | `evidence/TC-ST08-10-<product>.txt` |
| `TC-ST08-11` | Single-node topology | Identical parameters to TC-ST04-12. | NOT AVAILABLE | `evidence/TC-ST08-11-<product>.txt` |
| `TC-ST08-12` | Distributed topology | Identical parameters to TC-ST04-13. | NOT AVAILABLE | `evidence/TC-ST08-12-<product>.txt` |
| `TC-ST08-13` | NFS-backed storage | Identical parameters to TC-ST04-14. **Currently unavailable** — see Findings. | NOT AVAILABLE | `evidence/TC-ST08-13-<product>.txt` |
| `TC-ST08-14` | Repeated runs | Identical repetition count to TC-ST04-15; every repetition kept. | NOT AVAILABLE | `evidence/TC-ST08-14-<product>.txt` |
| `TC-ST08-15` | Noisy neighbour | Identical competing load to TC-ST04-16. | NOT AVAILABLE | `evidence/TC-ST08-15-<product>.txt` |
| `TC-ST08-16` | Resource limits | The same limits shown to be enforced on Silo, so neither product is measured unconstrained. | NOT AVAILABLE | `evidence/TC-ST08-16-<product>.txt` |
| `TC-ST08-17` | Method parity check | The ST04 and ST08 command lines are diffed and shown to differ only in the product alias. A failure here invalidates the comparison. | NOT AVAILABLE | `evidence/TC-ST08-17-<product>.txt` |

### Commands

```bash
# Parity check first: the two runs must differ only in the alias
diff <(sed 's/minio/PRODUCT/g' evidence/st04-commands.txt) \
     <(sed 's/silo/PRODUCT/g'   evidence/st08-commands.txt)

docker exec mc-client mc admin info silo                       # health before the run
docker run --rm --network migration-net \
  minio/warp:v1.3.1 mixed --bucket warp-bench \
  --distobject --size 64Mi --objects 500 --duration 60s
docker exec mc-client mc admin info silo                       # health after the run

docker compose -f lab/compose/storage/compose.yml run --rm fio
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
| `TC-ST08-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-09` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-10` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-11` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-12` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-13` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-14` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-15` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-16` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST08-17` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| ST04 parameters reused unchanged | NOT AVAILABLE | — |
| Method parity proven by command diff, not asserted | NOT AVAILABLE | — |
| Every repetition retained on both sides | NOT AVAILABLE | — |
| Resource limits enforced on Silo as on MinIO | NOT AVAILABLE | — |
| GOMAXPROCS asymmetry stated as a confound on every throughput comparison | NOT AVAILABLE | — |
| NFS case reported NOT AVAILABLE on both sides | NOT AVAILABLE | — |

## Findings and Problems

* Silo logs `WARN: Detected GOMAXPROCS(2) < NumCPU(4)` under the 0.80 CPU limit. Go
*   1.25+ derives GOMAXPROCS from the cgroup quota, while the Go 1.24-built MinIO does not.
*   This means the two products are **not** running on identical effective parallelism, and
*   any throughput difference is partly attributable to that rather than to the products
*   alone. This confound is restated beside every throughput comparison in this document and
  carried into the final recommendation.
* **NFS-backed storage is currently unavailable**, so TC-ST08-13 has no counterpart to
*   TC-ST04-14. The NFS server starts and exports correctly, but a client mount does not
*   complete: NFSv4 hangs uninterruptibly, including with `nolock`, and NFSv3 fails because
*   `rpc.statd` is required for remote locking. Both sides of that comparison are therefore
*   NOT AVAILABLE rather than estimated.
* `fio` throughput varied by roughly 25x between targets in ST04. Until that variance is
*   explained, `fio` output is a storage capability check on both sides, not a benchmark.

## Limitations / Assumptions

**Assumptions.**
* ST04's parameters are reused unchanged; this is checked by TC-ST08-17, not assumed.
* Both products run on the same host, same storage and same dataset, in separate passes.
* Every repetition is reported, and the spread is shown rather than reduced to a single figure.

**Limitations.**
* The host is below the reference configuration, so figures are below the reference configuration and are only meaningful next to ST04's, never as absolute performance.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. ST08 cannot be marked PASS or FAIL until every available case has run with ST04's parameters unchanged, verified by TC-ST08-17.

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
