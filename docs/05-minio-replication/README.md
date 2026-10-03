# DEV-909 — MinIO Replication

**Status:** Not Started
**Tracker:** `DEV-909`
**Epic:** `DEV-904`
**Legacy label:** DEV-909

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Prove that replication works and, more importantly, that it fails visibly.
A replication setup that silently loses objects is worse than no replication, so
this phase pairs every success case with a negative control.

## Scope

In scope: bucket replication, two-way replication, existing-object
replication, delete-marker replication, version replication, tag and metadata
replication, object-lock metadata replication, batch replication, site
replication, target outage, network cut, lag measurement, resync, and two-way
conflict behaviour.

Out of scope: distributed-mode healing ([`docs/04-minio-distributed-mode`](../04-minio-distributed-mode/README.md)), throughput comparison (ST04),
Silo behaviour (ST06), and client compatibility (ST07).

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

* Two MinIO deployments resident at the same time: a replication source and a replication target. This is MinIO-only co-residency; the prohibition is on mixing MinIO and Silo nodes in one cluster, which a pre-commit hook enforces.
* The dataset for this phase uses the reduced profile sized for two concurrent deployments; the measured size and the parity-2 on-disk amplification are recorded in *Environment* when the phase runs.
* Both deployments validated, and the source's replication credentials present in ignored local configuration.
* A seeded dataset on the source, so replication is proven against real objects.
* Versioning enabled on the source buckets, because version and delete-marker replication cannot be tested without it.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-DEV909-01` | Bucket replication baseline | An object written to the source appears on the target with matching size and checksum. | NOT AVAILABLE | `evidence/TC-DEV909-01-<product>.txt` |
| `TC-DEV909-02` | Existing-object replication | Objects written before replication was configured are replicated; which objects are in scope is recorded explicitly. | NOT AVAILABLE | `evidence/TC-DEV909-02-<product>.txt` |
| `TC-DEV909-03` | Two-way replication | A write on each side appears on the other; the propagation delay is recorded. | NOT AVAILABLE | `evidence/TC-DEV909-03-<product>.txt` |
| `TC-DEV909-04` | Version replication | Multiple versions on the source are all present on the target. | NOT AVAILABLE | `evidence/TC-DEV909-04-<product>.txt` |
| `TC-DEV909-05` | Delete-marker replication | Delete markers replicate, and the target's visible state matches the source's. | NOT AVAILABLE | `evidence/TC-DEV909-05-<product>.txt` |
| `TC-DEV909-06` | Tag and metadata replication | Object tags and metadata arrive on the target byte-identical to the source. | NOT AVAILABLE | `evidence/TC-DEV909-06-<product>.txt` |
| `TC-DEV909-07` | Object-lock metadata replication | Lock configuration and retention arrive on the target and are enforced there. | NOT AVAILABLE | `evidence/TC-DEV909-07-<product>.txt` |
| `TC-DEV909-08` | Batch replication | A batch operation replicates; partial failure is reported per object rather than silently dropped. | NOT AVAILABLE | `evidence/TC-DEV909-08-<product>.txt` |
| `TC-DEV909-09` | Site replication | Site replication brings up a peer and the required site objects replicate. | NOT AVAILABLE | `evidence/TC-DEV909-09-<product>.txt` |
| `TC-DEV909-10` | Target outage | The target is stopped; writes on the source continue and are queued, not lost. | NOT AVAILABLE | `evidence/TC-DEV909-10-<product>.txt` |
| `TC-DEV909-11` | Network cut | A network cut between deployments is recovered from without manual repair. | NOT AVAILABLE | `evidence/TC-DEV909-11-<product>.txt` |
| `TC-DEV909-12` | Lag measurement | Replication lag is measured with its sampling interval and measurement point stated. | NOT AVAILABLE | `evidence/TC-DEV909-12-<product>.txt` |
| `TC-DEV909-13` | Resync | A target that fell behind resynchronises and is re-verified against the source. | NOT AVAILABLE | `evidence/TC-DEV909-13-<product>.txt` |
| `TC-DEV909-14` | Two-way conflict behaviour | Concurrent writes to the same key produce a recorded, deterministic outcome rather than silent divergence. | NOT AVAILABLE | `evidence/TC-DEV909-14-<product>.txt` |
| `TC-DEV909-15` | Negative control — missing object detected | An object removed from the target without going through replication is detected by the manifest comparison. | NOT AVAILABLE | `evidence/TC-DEV909-15-<product>.txt` |
| `TC-DEV909-16` | Negative control — altered object detected | An object's bytes are altered directly on the target and the checksum comparison detects it. | NOT AVAILABLE | `evidence/TC-DEV909-16-<product>.txt` |

### Commands

```bash
# The target is a second, separate MinIO deployment - never a Silo node.
# It needs its own compose project and its own credentials in ignored local config.
docker compose -f lab/compose/minio/compose.yml up -d            # source
docker compose -f lab/compose/replication-target/compose.yml up -d  # target

# Enable replication on the source, including the object classes under test
docker exec mc-client mc admin replicate add minio/eval-src \
  --remote-bucket 'http://<target>:9000/eval-dst' --replicate \
  tags,metadata,deleteMarker,versioning,existingObjects

# Negative control: alter the target outside replication, then prove detection
printf tampered > /tmp/tampered
docker cp /tmp/tampered mc-client:/tmp/tampered
docker exec mc-client mc pipe minio/eval-dst/<key> < /tmp/tampered

# The comparison MUST report the mismatch; an empty report means the check is broken
tools/bin/verify-manifest minio eval-dst manifest-dst.jsonl   # must report the mismatch
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
| `TC-DEV909-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-09` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-10` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-11` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-12` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-13` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-14` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-15` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-DEV909-16` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| Every replication mode exercised with raw output | NOT AVAILABLE | — |
| Negative controls prove the manifest comparison detects a missing object | NOT AVAILABLE | — |
| Negative controls prove it detects an altered object | NOT AVAILABLE | — |
| Target outage and network cut recovered without manual repair | NOT AVAILABLE | — |
| Conflict behaviour recorded as observed, not as desired | NOT AVAILABLE | — |

## Findings and Problems

* A COMPLIANCE-locked object on the source cannot be deleted, and a bucket holding one
*   cannot be removed even with `mc rb --force --dangerous`, for the retention lifetime.
*   Replicated lock metadata therefore makes the target bucket equally undeletable; each
*   negative-control run needs a fresh bucket name.
* Two MinIO deployments resident simultaneously is a deliberate exception to the
*   one-heavy-cluster-at-a-time rule, and is confined to this phase. The pre-commit
*   `check-no-mixed-cluster` hook still enforces that no single cluster mixes
*   products, and it runs on every commit.

## Limitations / Assumptions

**Assumptions.**
* The replication target is a separate MinIO deployment, never a Silo node; mixing products in one cluster is prevented by a pre-commit hook.
* The reduced dataset profile is used so two deployments fit the available memory.
* Replication is asynchronous, so every success case has an explicit convergence wait with the observed delay recorded.

**Limitations.**
* The host is below the reference configuration, so lag figures are indicative and are affected by the reduced dataset and the shared host.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. DEV-909 cannot be marked PASS or FAIL until the positive cases replicate correctly and both negative controls are shown to detect divergence.

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
