# ST05 — MinIO Distributed Mode, Healing and Rebalancing

**Status:** Not Started
**Tracker:** `DEV-908`
**Epic:** `DEV-904`
**Legacy label:** ST05 (this directory)

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Establish what the MinIO erasure pool actually does when nodes, drives or
network connectivity are removed, and how it recovers.

Distributed behaviour is the main reason to run MinIO rather than a plain S3
service, so this phase is treated as a correctness requirement rather than a
performance one: healing correctness is established here, healing timing is
measured in ST04.

## Scope

In scope: node failure, drive loss and wipe, parity exceedance, network
partition, rolling restart, automatic heal, manual heal, pool expansion, pool
decommission, rebalance, volume reattachment, and shared-volume protection.

Out of scope: replication (DEV-909, tracked separately in `docs/05`), throughput
measurement (ST04), Silo behaviour (ST06), and client compatibility (ST07).

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

* ST01 and ST03 complete for the MinIO cluster.
* A verified baseline: cluster healthy, `Pool: 1`, `Network: 4/4 OK`, `Drives: 1/1 OK` on every node, captured to `evidence/`.
* A seeded dataset so recovery is proven against real objects, not an empty pool.
* `tools/bin/lab` available to stop and start individual nodes without touching the shared network.
* The `proxy` health endpoint `/healthz` is available, so balancer health survives a deliberate backend outage.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-ST05-01` | Baseline pool state | All four nodes report `Network: 4/4 OK`, `Drives: 1/1 OK`, `Pool: 1` before any fault is injected. | NOT AVAILABLE | `evidence/TC-ST05-01-<product>.txt` |
| `TC-ST05-02` | Single node failure | One node is stopped; remaining nodes stay online and the cluster reports reduced but available status. | NOT AVAILABLE | `evidence/TC-ST05-02-<product>.txt` |
| `TC-ST05-03` | Drive loss | One drive is removed; the pool reports the drive offline and continues serving reads and writes. | NOT AVAILABLE | `evidence/TC-ST05-03-<product>.txt` |
| `TC-ST05-04` | Drive wipe | A drive is wiped with recorded contents; behaviour matches the drive-loss case, with the wipe method recorded. | NOT AVAILABLE | `evidence/TC-ST05-04-<product>.txt` |
| `TC-ST05-05` | Parity exceedance | More drives are removed than the parity allows; the exact point at which writes stop is recorded, because that boundary is the durability limit. | NOT AVAILABLE | `evidence/TC-ST05-05-<product>.txt` |
| `TC-ST05-06` | Network partition | One node is isolated from the network; its exclusion from quorum is captured. | NOT AVAILABLE | `evidence/TC-ST05-06-<product>.txt` |
| `TC-ST05-07` | Rolling restart | Nodes are restarted one at a time; the cluster never drops below quorum during the cycle. | NOT AVAILABLE | `evidence/TC-ST05-07-<product>.txt` |
| `TC-ST05-08` | Automatic heal | A returned node rejoins and the pool heals automatically; the heal completes without operator action. | NOT AVAILABLE | `evidence/TC-ST05-08-<product>.txt` |
| `TC-ST05-09` | Manual heal | Heal is triggered explicitly; the command, its output and the resulting state are recorded. | NOT AVAILABLE | `evidence/TC-ST05-09-<product>.txt` |
| `TC-ST05-10` | Heal timing | Time from fault to full health is measured, with start and end conditions stated. | NOT AVAILABLE | `evidence/TC-ST05-10-<product>.txt` |
| `TC-ST05-11` | Pool expansion | An additional drive set is added; the new pool forms and the drive count rises as expected. | NOT AVAILABLE | `evidence/TC-ST05-11-<product>.txt` |
| `TC-ST05-12` | Pool decommission | A set is removed; the pool count falls and the cluster remains healthy. | NOT AVAILABLE | `evidence/TC-ST05-12-<product>.txt` |
| `TC-ST05-13` | Rebalance | Data is redistributed after expansion or decommission; progress and final drive usage captured. | NOT AVAILABLE | `evidence/TC-ST05-13-<product>.txt` |
| `TC-ST05-14` | Volume reattachment | A previously detached volume is reattached and its objects are readable again. | NOT AVAILABLE | `evidence/TC-ST05-14-<product>.txt` |
| `TC-ST05-15` | Shared-volume protection | Attempting to attach the same volume to two nodes is refused. | NOT AVAILABLE | `evidence/TC-ST05-15-<product>.txt` |
| `TC-ST05-16` | Data integrity after recovery | A checksum comparison against the pre-fault manifest shows zero mismatches for surviving objects. | NOT AVAILABLE | `evidence/TC-ST05-16-<product>.txt` |

### Commands

```bash
# Capture the healthy baseline first - every fault case is relative to it
./tools/bin/st01-verify minio > evidence/TC-ST05-01-minio.txt

# Inject one fault at a time, one case at a time
docker compose -f lab/compose/minio/compose.yml stop node-1
docker exec mc-client mc admin heal -r minio
docker exec mc-client mc admin info minio

# Restart the injected fault, then prove data survived
docker compose -f lab/compose/minio/compose.yml start node-1
tools/bin/verify-manifest minio eval-seed lab/data/dataset/dataset-manifest.jsonl
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
| `TC-ST05-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-09` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-10` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-11` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-12` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-13` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-14` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-15` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST05-16` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| Baseline captured before any fault injection | NOT AVAILABLE | — |
| Every fault case injected and recovered individually | NOT AVAILABLE | — |
| Parity-exceedance boundary located and recorded | NOT AVAILABLE | — |
| Heal completion proven by health output, not by elapsed time alone | NOT AVAILABLE | — |
| Post-recovery checksum comparison shows zero mismatches | NOT AVAILABLE | — |

## Findings and Problems

* `lb-silo` crash-looped when started without its cluster because nginx resolves
*   upstream hostnames at config load. A `/healthz` endpoint was added so proxy health no
*   longer depends on a live upstream — needed here, because this phase takes backends down
*   deliberately. Recorded in ST01 finding 9.4.
* Silo logs `WARN: Detected GOMAXPROCS(2) < NumCPU(4)` under the 0.80 CPU limit because
*   Go 1.25+ derives GOMAXPROCS from the cgroup quota, while Go 1.24-built MinIO does not.
*   The two products therefore do not run on identical effective parallelism, which
*   must be stated beside any throughput difference rather than attributed to either
*   product.

## Limitations / Assumptions

**Assumptions.**
* Fault injection is confined to the MinIO cluster; pre-existing containers belonging to other stacks are never stopped.
* Each fault is applied to a cluster that was verified healthy immediately beforehand.
* Only one fault is active at a time, so an observed behaviour is attributable to that fault.

**Limitations.**
* The host is below the reference configuration, so heal timing is indicative and is not comparable to a reference host.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. ST05 cannot be marked PASS or FAIL until every fault case has been injected, recovered and proven by checksum comparison.

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
