# ST04 — MinIO Performance Baseline

**Status:** Not Started
**Tracker:** `DEV-910`
**Epic:** `DEV-904`
**Legacy label:** ST04 (this directory)

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Establish the MinIO performance baseline that DEV-913 later compares
against, using a documented, repeatable measurement method.

The method matters more than the absolute numbers here. The host is below the
reference configuration, so these numbers cannot support a recommendation on
their own; they can support a like-for-like comparison, which is what DEV-913
needs.

## Scope

In scope: small-object PUT/GET/DELETE/LIST, large-object PUT/GET, mixed
workloads, multipart, versioned workloads, single-node and distributed
topologies, local storage, NFS-backed storage where available, repeated runs, a
noisy-neighbour case, resource-limit enforcement, and raw disk `fio`.

Out of scope: the Silo side of the comparison (ST08, [`docs/09-silo-performance-comparison`](../09-silo-performance-comparison/README.md)), functional
behaviour (ST03/ST06), and the final recommendation (ST10).

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

* ST02 complete: the Profile B dataset is generated and seeded, and `tools/bin/verify-manifest` reports zero mismatches.
* The dataset size meets the Profile B floor of 5 GB. The earlier 886 MiB / 669-object iteration is superseded and is not valid input.
* The cluster's health is verified immediately before each run, and the run is discarded if the cluster degraded during it.
* `warp` parameters are fixed and written into the report before the runs; no parameter is chosen after seeing a result.
* Repetitions are stated per case, and every repetition is kept, including slow ones.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-ST04-01` | Raw disk sequential write | `fio` measures the storage under the cluster data directories, not the object API, so storage capability is separated from server overhead. | NOT AVAILABLE | `evidence/TC-ST04-01-<product>.txt` |
| `TC-ST04-02` | Raw disk random write and read | Random 4k IOPS and latency, recorded per storage target. | NOT AVAILABLE | `evidence/TC-ST04-02-<product>.txt` |
| `TC-ST04-03` | Small-object PUT | Sustained small-object write throughput and latency at the stated object size. | NOT AVAILABLE | `evidence/TC-ST04-03-<product>.txt` |
| `TC-ST04-04` | Small-object GET | Read throughput and latency at the same object size. | NOT AVAILABLE | `evidence/TC-ST04-04-<product>.txt` |
| `TC-ST04-05` | Small-object DELETE | Delete throughput at the same object size. | NOT AVAILABLE | `evidence/TC-ST04-05-<product>.txt` |
| `TC-ST04-06` | Object LIST | LIST throughput against a bucket of the stated object count. | NOT AVAILABLE | `evidence/TC-ST04-06-<product>.txt` |
| `TC-ST04-07` | Large-object PUT | Single large-object write throughput. | NOT AVAILABLE | `evidence/TC-ST04-07-<product>.txt` |
| `TC-ST04-08` | Large-object GET | Single large-object read throughput. | NOT AVAILABLE | `evidence/TC-ST04-08-<product>.txt` |
| `TC-ST04-09` | Mixed workload | A mixed PUT/GET/DELETE/LIST profile, with the mix ratio stated. | NOT AVAILABLE | `evidence/TC-ST04-09-<product>.txt` |
| `TC-ST04-10` | Multipart upload | Multipart throughput at the stated part size and count. | NOT AVAILABLE | `evidence/TC-ST04-10-<product>.txt` |
| `TC-ST04-11` | Versioned workload | Throughput with versioning enabled, which adds per-version write cost. | NOT AVAILABLE | `evidence/TC-ST04-11-<product>.txt` |
| `TC-ST04-12` | Single-node topology | The same workload against one node, to separate topology cost from storage cost. | NOT AVAILABLE | `evidence/TC-ST04-12-<product>.txt` |
| `TC-ST04-13` | Distributed topology | The same workload against the 4-node pool. | NOT AVAILABLE | `evidence/TC-ST04-13-<product>.txt` |
| `TC-ST04-14` | NFS-backed storage | The same workload against the NFS mount. **Currently unavailable** — see Findings. | NOT AVAILABLE | `evidence/TC-ST04-14-<product>.txt` |
| `TC-ST04-15` | Repeated runs | Each case is repeated the stated number of times and every repetition is reported. | NOT AVAILABLE | `evidence/TC-ST04-15-<product>.txt` |
| `TC-ST04-16` | Noisy neighbour | A competing CPU and IO load runs alongside; the degradation is recorded rather than averaged away. | NOT AVAILABLE | `evidence/TC-ST04-16-<product>.txt` |
| `TC-ST04-17` | Resource limits | The configured CPU and memory limits are shown to be enforced, so a limit is not silently ignored. | NOT AVAILABLE | `evidence/TC-ST04-17-<product>.txt` |
| `TC-ST04-18` | Result reproducibility | A clean-machine rerun of one case reproduces the first run within the stated tolerance. | NOT AVAILABLE | `evidence/TC-ST04-18-<product>.txt` |

### Commands

```bash
# Raw storage capability, before the object layer is involved
docker compose -f lab/compose/storage/compose.yml run --rm fio

# Object-layer workload with fixed, pre-declared parameters
docker exec mc-client mc admin info minio                       # health before the run
docker run --rm --network migration-net \
  minio/warp:v1.3.1 mixed --bucket warp-bench \
  --distobject --size 64Mi --objects 500 --duration 60s
docker exec mc-client mc admin info minio                       # health after the run

# Discards a run if the cluster degraded, rather than reporting it as a slow result
docker exec mc-client mc admin heal -r minio                    # expect 'not needed'
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
| `TC-ST04-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-09` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-10` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-11` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-12` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-13` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-14` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-15` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-16` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-17` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST04-18` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| Parameters and repetitions declared before execution | NOT AVAILABLE | — |
| Every repetition retained, including outliers | NOT AVAILABLE | — |
| Cluster health verified before and after each run | NOT AVAILABLE | — |
| Resource limits shown to be enforced | NOT AVAILABLE | — |
| fio variance reported as an unresolved issue, not smoothed into a single figure | NOT AVAILABLE | — |
| NFS case reported NOT AVAILABLE with the specific mount failure named | NOT AVAILABLE | — |

## Findings and Problems

* **NFS-backed storage is currently unavailable and this case cannot pass.** The NFS
*   server starts and exports correctly and port 2049 answers, but a client mount does not
*   complete: NFSv4 hangs uninterruptibly, including with `nolock`, and NFSv3 fails because
*   `rpc.statd` is required for remote locking. The server-side fix was to drop `rpcbind` and
*   run `rpc.nfsd` with NFSv4 only. The remaining fault is client-side, so TC-ST04-14 is
*   reported as NOT AVAILABLE with this reason rather than worked around. Any NFS-backed
*   DEV-910 comparison is unavailable for the same reason.
* 
* `fio` throughput varied by roughly 25x between targets (about 1,560,000, 64,000 and
*   167,000 KiB/s across container and bind-mount targets). That spread is far too large to
*   report as a benchmark result, so the recorded `fio` output is treated as a **storage
*   capability check** only, and the variance is reported as an open issue rather than a number.
*   It is explained by the targets being different filesystems, and it is not resolved.
* 
* Silo logs `WARN: Detected GOMAXPROCS(2) < NumCPU(4)` under the 0.80 CPU limit, because
*   Go 1.25+ derives GOMAXPROCS from the cgroup quota while Go 1.24-built MinIO does not.
*   Any throughput comparison must state this, so it is not attributed to either product.

## Limitations / Assumptions

**Assumptions.**
* All parameters, repetitions and durations are fixed before the first run and are not adjusted afterwards.
* One heavy cluster runs at a time, and the other product's containers are stopped before each run.
* Results are reported with their full distribution across repetitions, not a best-of or a single favourable run.

**Limitations.**
* The host is below the reference configuration, so throughput and latency figures are not comparable to a reference host, and are only meaningful against DEV-913's identically measured Silo run.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. ST04 cannot be marked PASS or FAIL until every available case has run with declared parameters and retained repetitions. TC-ST04-14 stays NOT AVAILABLE while the NFS client mount fails.

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
