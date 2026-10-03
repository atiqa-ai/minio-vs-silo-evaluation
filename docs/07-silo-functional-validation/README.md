# ST06 — Silo Functional Validation

**Status:** Not Started
**Tracker:** `DEV-911`
**Epic:** `DEV-904`
**Legacy label:** ST06

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Run the ST03 functional test set against the Silo cluster under identical
parameters, so the two products' functional surfaces are compared on the same
tests rather than on impressions.

A difference recorded here is a candidate finding. It only becomes a finding
after it is reproduced and its cause is identified in ST07.

## Scope

In scope: the same functional S3, access control, encryption and
transport, and object-behaviour cases defined in ST03, executed against Silo.

Out of scope: throughput and latency (ST08), distributed healing and replication
(ST05, DEV-909), client and SDK differences (ST07), and security review (ST09).

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

* ST03 complete, with its expected results and evidence already on file, so the same cases can be run unchanged.
* MinIO fully stopped before Silo starts; only one heavy cluster runs at a time.
* `tools/bin/lab up silo` brings up four healthy Silo nodes and a healthy `lb-silo`.
* The dataset is the same bytes as ST03. It is regenerated, never copied between products.
* `silo-client` running so `mcli` is available inside the Silo image.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-ST06-01` | Bucket create, list and delete | The same operation sequence run against Silo, with the same expected result and any difference recorded. | NOT AVAILABLE | `evidence/TC-ST06-01-<product>.txt` |
| `TC-ST06-02` | Object round-trip | Put, get, head and delete against Silo, with size and checksum compared to the same source object. | NOT AVAILABLE | `evidence/TC-ST06-02-<product>.txt` |
| `TC-ST06-03` | Server-side copy | Copy behaviour against Silo, compared to the MinIO result from ST03. | NOT AVAILABLE | `evidence/TC-ST06-03-<product>.txt` |
| `TC-ST06-04` | Multipart upload | Multipart behaviour against Silo, including whether part size and count are accepted as MinIO accepts them. | NOT AVAILABLE | `evidence/TC-ST06-04-<product>.txt` |
| `TC-ST06-05` | Range reads | Range behaviour against Silo, including the out-of-range error. | NOT AVAILABLE | `evidence/TC-ST06-05-<product>.txt` |
| `TC-ST06-06` | Presigned URLs | Presigned URL behaviour against Silo, including post-expiry rejection. | NOT AVAILABLE | `evidence/TC-ST06-06-<product>.txt` |
| `TC-ST06-07` | ListObjects v1 and v2 | Both list versions against Silo, compared key-set-for-key-set with ST03. | NOT AVAILABLE | `evidence/TC-ST06-07-<product>.txt` |
| `TC-ST06-08` | Batch delete | Batch behaviour against Silo, including per-key error reporting. | NOT AVAILABLE | `evidence/TC-ST06-08-<product>.txt` |
| `TC-ST06-09` | Object metadata | Metadata storage and read-back against Silo, using the `;` separator form, compared to ST03. | NOT AVAILABLE | `evidence/TC-ST06-09-<product>.txt` |
| `TC-ST06-10` | Object tags | Tag syntax against Silo, including the comma, `&` and space forms, compared to the ST03 table. | NOT AVAILABLE | `evidence/TC-ST06-10-<product>.txt` |
| `TC-ST06-11` | Bucket tags | Bucket tag behaviour against Silo. | NOT AVAILABLE | `evidence/TC-ST06-11-<product>.txt` |
| `TC-ST06-12` | Bucket policy | Policy enforcement against Silo, with the denied request captured. | NOT AVAILABLE | `evidence/TC-ST06-12-<product>.txt` |
| `TC-ST06-13` | IAM | IAM users, groups and policies against Silo, including whether revocation takes effect. | NOT AVAILABLE | `evidence/TC-ST06-13-<product>.txt` |
| `TC-ST06-14` | Service accounts | Service account behaviour against Silo, including expiry. | NOT AVAILABLE | `evidence/TC-ST06-14-<product>.txt` |
| `TC-ST06-15` | STS | STS behaviour against Silo, including whether it is available at all. | NOT AVAILABLE | `evidence/TC-ST06-15-<product>.txt` |
| `TC-ST06-16` | Anonymous access | Default anonymous denial and prefix-scoped anonymous read against Silo. | NOT AVAILABLE | `evidence/TC-ST06-16-<product>.txt` |
| `TC-ST06-17` | TLS | TLS behaviour against Silo, with protocol and cipher recorded for comparison. | NOT AVAILABLE | `evidence/TC-ST06-17-<product>.txt` |
| `TC-ST06-18` | SSE-S3 | SSE-S3 support on Silo, confirmed by read-back rather than by a successful upload. | NOT AVAILABLE | `evidence/TC-ST06-18-<product>.txt` |
| `TC-ST06-19` | SSE-C | SSE-C support on Silo, including whether a wrong customer key is rejected. | NOT AVAILABLE | `evidence/TC-ST06-19-<product>.txt` |
| `TC-ST06-20` | Versioning lifecycle | Enable, suspend and re-enable against Silo, including whether delete markers are created as MinIO creates them. | NOT AVAILABLE | `evidence/TC-ST06-20-<product>.txt` |
| `TC-ST06-21` | Multiple versions and delete markers | Version listing and marker behaviour against Silo. | NOT AVAILABLE | `evidence/TC-ST06-21-<product>.txt` |
| `TC-ST06-22` | Restore a previous version | Version restore against Silo, or a recorded statement that it is unsupported. | NOT AVAILABLE | `evidence/TC-ST06-22-<product>.txt` |
| `TC-ST06-23` | Permanent version delete | Permanent version deletion against Silo. | NOT AVAILABLE | `evidence/TC-ST06-23-<product>.txt` |
| `TC-ST06-24` | Object lock governance | GOVERNANCE retention on Silo, including whether privileged bypass exists. | NOT AVAILABLE | `evidence/TC-ST06-24-<product>.txt` |
| `TC-ST06-25` | Object lock compliance | COMPLIANCE retention on Silo, including whether it blocks deletion and bucket removal. | NOT AVAILABLE | `evidence/TC-ST06-25-<product>.txt` |
| `TC-ST06-26` | Retention extension and bypass | Extension and bypass behaviour against Silo. | NOT AVAILABLE | `evidence/TC-ST06-26-<product>.txt` |
| `TC-ST06-27` | Legal hold | Legal hold place, hold and release against Silo. | NOT AVAILABLE | `evidence/TC-ST06-27-<product>.txt` |
| `TC-ST06-28` | Default retention | Default bucket retention on Silo. | NOT AVAILABLE | `evidence/TC-ST06-28-<product>.txt` |
| `TC-ST06-29` | Lifecycle expiry | Lifecycle expiry on Silo, observed over time. | NOT AVAILABLE | `evidence/TC-ST06-29-<product>.txt` |
| `TC-ST06-30` | Delete-marker cleanup | Delete-marker cleanup on Silo. | NOT AVAILABLE | `evidence/TC-ST06-30-<product>.txt` |

### Commands

```bash
# MinIO must be fully down before Silo starts
./tools/bin/lab down minio
./tools/bin/lab up silo && ./tools/bin/lab up proxy

docker exec silo-client mcli alias set silo http://lb-silo:80 \
  "$SILO_ROOT_USER" "$SILO_ROOT_PASSWORD"

# Same case identifiers as ST03, so the two result tables can be compared row by row
docker exec silo-client mcli ls --versions silo/<bucket>
docker exec silo-client mcli stat silo/<bucket>/<key>

# Silo has no `mc checksum`; this is the verification cross-check ST02 also records
docker exec silo-client mcli checksum verify \
  --manifest manifest-silo.jsonl --report evidence/checksum-silo.jsonl
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
| `TC-ST06-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-09` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-10` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-11` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-12` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-13` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-14` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-15` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-16` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-17` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-18` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-19` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-20` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-21` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-22` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-23` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-24` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-25` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-26` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-27` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-28` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-29` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST06-30` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| Every ST03 case executed against Silo with the same case identifier | NOT AVAILABLE | — |
| Differences from ST03 recorded case by case, not summarised | NOT AVAILABLE | — |
| Unsupported behaviour recorded with the error output | NOT AVAILABLE | — |
| Each difference confirmed against the raw evidence before being called a difference | NOT AVAILABLE | — |
| No case closed on a successful exit code alone | NOT AVAILABLE | — |

## Findings and Problems

* `mcli` uses `&` to separate object tags and also rejects the AWS comma form, so the
*   two clients agree on that point and the AWS-documented comma syntax is wrong for both.
*   Already measured in ST02 finding 9.3; re-confirmed here rather than assumed.
* `mc` has no `checksum` command, so checksum verification is Silo-only via `mcli`. This
*   asymmetry is itself a recorded client difference, not a skipped test.
* Silo accepts `minio server ...` and bare `server ...` as aliases for its server binary.
*   Noted in ST01 and relevant here because a Silo deployment can therefore be started with
*   MinIO syntax; the lab uses the explicit `silo` form so it does not depend on that alias.
* `silo --commit` and `mcli --commit` are **not** valid flags, although MinIO accepts
*   `--commit`. The commit is still visible in `--version` output. A real, minor CLI surface
*   difference, recorded rather than worked around.

## Limitations / Assumptions

**Assumptions.**
* The identical dataset is regenerated rather than copied between products, so neither product benefits from a warm copy.
* The identical case identifiers and identical parameters are used as in ST03.
* Any behaviour Silo does not implement is recorded as unsupported with the error captured, not omitted.

**Limitations.**
* The host is below the reference configuration, so results are indicative and establish functional behaviour only, not performance.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. ST06 cannot be marked PASS or FAIL until every ST03 case has been run against Silo with its raw output in `evidence/`.

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
