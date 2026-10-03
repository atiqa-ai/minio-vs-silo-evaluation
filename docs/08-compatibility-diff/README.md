# ST07 — S3 and Client Compatibility

**Status:** Not Started
**Tracker:** `DEV-912`
**Epic:** `DEV-904`
**Legacy label:** ST07

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Turn the differences noticed while building the tooling into a documented,
reproducible compatibility report, and test the O01-O08 vendor claims
independently rather than accepting them.

Compatibility risk is what most often decides a migration, and it is the area
where an unverified claim causes the most damage.

## Scope

In scope: conditional requests, conditional DELETE, batch delete,
multipart-list prefix behaviour, unsupported APIs, checksums, error codes and
messages, SDKs, `mc` versus `mcli`, client tooling actually used including
Terraform, Prometheus metric compatibility, and dashboards and alerts.

In scope for independent testing: claims O01 through O08, tested against both
products and reported as confirmed, partially confirmed, or not confirmed.

Out of scope: throughput and latency (ST04, ST08), security review (ST09), and
the final recommendation (ST10).

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

* ST03 and ST06 complete, so the functional differences are already known and this phase explains rather than rediscovers them.
* The list of client tooling the migration will actually use, confirmed rather than assumed.
* Both clusters available, run in separate passes with identical parameters.
* `mcli checksum verify` available for the Silo checksum comparison.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-ST07-01` | O01 claim — independent test | Each vendor claim is tested on its own terms and reported as confirmed, partially confirmed, or not confirmed. | NOT AVAILABLE | `evidence/TC-ST07-01-<product>.txt` |
| `TC-ST07-02` | Conditional requests | `If-None-Match` and `If-Modified-Since` behave identically on both products, or the divergence is recorded. | NOT AVAILABLE | `evidence/TC-ST07-02-<product>.txt` |
| `TC-ST07-03` | Conditional DELETE | `If-Match` on delete behaves consistently, or the divergence is recorded. | NOT AVAILABLE | `evidence/TC-ST07-03-<product>.txt` |
| `TC-ST07-04` | Batch delete | `DeleteObjects` semantics, limits and error reporting compared. | NOT AVAILABLE | `evidence/TC-ST07-04-<product>.txt` |
| `TC-ST07-05` | Multipart list prefix behaviour | Multipart listing with prefixes compared; a divergence here silently breaks large-bucket migrations. | NOT AVAILABLE | `evidence/TC-ST07-05-<product>.txt` |
| `TC-ST07-06` | Unsupported APIs | APIs absent on either product are enumerated rather than discovered during a migration. | NOT AVAILABLE | `evidence/TC-ST07-06-<product>.txt` |
| `TC-ST07-07` | Checksums | Checksum algorithm support and verification compared, including the `mcli` versus `mc` asymmetry. | NOT AVAILABLE | `evidence/TC-ST07-07-<product>.txt` |
| `TC-ST07-08` | Error codes and messages | Error codes compared for the same fault; message wording is compared separately from status codes. | NOT AVAILABLE | `evidence/TC-ST07-08-<product>.txt` |
| `TC-ST07-09` | SDK compatibility | The SDKs in use are exercised against both products and their behaviour compared. | NOT AVAILABLE | `evidence/TC-ST07-09-<product>.txt` |
| `TC-ST07-10` | `mc` versus `mcli` | Client surface differences tabulated, including commands present on one and absent on the other. | NOT AVAILABLE | `evidence/TC-ST07-10-<product>.txt` |
| `TC-ST07-11` | Terraform and other client tooling | The tooling actually used is run against both products. | NOT AVAILABLE | `evidence/TC-ST07-11-<product>.txt` |
| `TC-ST07-12` | Prometheus metric compatibility | Metric names compared one by one, so a dashboard does not silently lose series on migration. | NOT AVAILABLE | `evidence/TC-ST07-12-<product>.txt` |
| `TC-ST07-13` | Dashboards and alerts | Dashboards and alerts are exercised against each product and any missing series is recorded. | NOT AVAILABLE | `evidence/TC-ST07-13-<product>.txt` |

### Commands

```bash
# The MinIO client runs against both products, which is the point of this phase
docker exec mc-client mc alias set minio http://lb-minio:80 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
docker exec mc-client mc alias set silo   http://lb-silo:80   "$SILO_ROOT_USER"   "$SILO_ROOT_PASSWORD"

# Metric compatibility, compared name by name rather than by dashboard appearance
docker exec mc-client mc admin prometheus metrics minio | sort > evidence/minio-metrics.txt
docker exec mc-client mc admin prometheus metrics silo   | sort > evidence/silo-metrics.txt
comm -3 evidence/minio-metrics.txt evidence/silo-metrics.txt > evidence/metric-diff.txt

# Checksum asymmetry: only Silo has a client-side verify command
docker exec silo-client mcli checksum verify --manifest manifest-silo.jsonl
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
| `TC-ST07-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-09` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-10` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-11` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-12` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST07-13` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| O01-O08 each reported as confirmed, partially confirmed, or not confirmed | NOT AVAILABLE | — |
| Every difference backed by reproducible evidence | NOT AVAILABLE | — |
| Error status codes compared separately from message wording | NOT AVAILABLE | — |
| Prometheus metric names compared individually, not by dashboard appearance | NOT AVAILABLE | — |
| Unsupported APIs enumerated, not left to be discovered during a migration | NOT AVAILABLE | — |

## Findings and Problems

* Measured and already recorded, to be confirmed here rather than rediscovered:
* 
* * `mc cp --attr` uses `;` to separate metadata headers; a comma merges them into one header
*   value, and repeating the flag keeps only the last attribute.
* * `mc` object tags require `&`. The AWS comma form errors; the space form exits 0 and stores a
*   single corrupted tag whose value contains `b=2`. An operator following the apparent syntax
*   gets corrupted data with no error.
* * `mc` has no `checksum` command, so checksum verification is Silo-only via `mcli`.
* * `mcli --commit` is not a valid flag, though the commit appears in `--version` output.

## Limitations / Assumptions

**Assumptions.**
* Client tooling is whatever the migration actually uses; the list is confirmed before the phase runs, not guessed.
* Both products are addressed through the same client where that is possible, so the variable under test is the server, not the client.
* A difference is reported only when it is reproducible from the evidence, not from a single observation.

**Limitations.**
* The host is below the reference configuration, so compatibility is assessed against the versions pinned in ST01; other versions may differ.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. ST07 cannot be marked PASS or FAIL until the O01-O08 claims are independently tested and every compatibility difference is reproduced from evidence.

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
