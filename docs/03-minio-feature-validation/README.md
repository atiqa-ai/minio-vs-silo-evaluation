# ST03 — MinIO Feature Validation

**Status:** Not Started
**Tracker:** `DEV-907`
**Epic:** `DEV-904`
**Legacy label:** ST03

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Validate MinIO CE against the S3 and object-storage behaviours the evaluation
depends on, so that later phases can treat MinIO's feature surface as a known,
evidenced baseline rather than an assumption.

Every capability exercised here is also exercised against Silo in ST06, under
identical parameters, so the two phases together form the functional comparison.

## Scope

In scope: functional S3 operations, access control, encryption and transport, and
object behaviour — versioning, delete markers, object lock, retention, legal
hold, and lifecycle expiry — measured on the MinIO cluster.

Out of scope: distributed-mode fault injection and healing (ST05), replication
(DEV-909), throughput and latency measurement (ST04), Silo behaviour (ST06),
client and SDK compatibility differences (ST07), and security review (ST09).

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

* ST01 complete: `migration-net` exists and all Compose projects validate.
* `tools/bin/lab up minio` brings up four healthy nodes and a healthy `lb-minio`.
* Synthetic credentials in `lab/compose/.env` (never committed).
* MinIO cluster left running; ST01 requires the MinIO baseline to be up for every test from ST02 onwards.
* Test bucket created with object lock enabled, which cannot be added to an existing bucket.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-ST03-01` | Bucket create, list and delete | Bucket is created, appears in the list, and is removed; the same result on a locked bucket is recorded rather than assumed. | NOT AVAILABLE | `evidence/TC-ST03-01-<product>.txt` |
| `TC-ST03-02` | Put, get, head and delete an object | Object round-trips with identical size and checksum; `head` returns the stored metadata; delete is confirmed absent. | NOT AVAILABLE | `evidence/TC-ST03-02-<product>.txt` |
| `TC-ST03-03` | Server-side copy | Copied object has a distinct key, identical content and checksum, and independent retention. | NOT AVAILABLE | `evidence/TC-ST03-03-<product>.txt` |
| `TC-ST03-04` | Multipart upload | Parts upload, complete, and the assembled object matches the source checksum; part count and size recorded. | NOT AVAILABLE | `evidence/TC-ST03-04-<product>.txt` |
| `TC-ST03-05` | Range reads | Byte ranges return exactly the requested bytes; an out-of-range request returns the documented error. | NOT AVAILABLE | `evidence/TC-ST03-05-<product>.txt` |
| `TC-ST03-06` | Presigned URLs | A presigned GET within the expiry returns the object; the same URL after expiry is rejected. | NOT AVAILABLE | `evidence/TC-ST03-06-<product>.txt` |
| `TC-ST03-07` | ListObjects v1 and v2 | Both list versions return the same key set for the same prefix; delimiter and prefix behaviour recorded. | NOT AVAILABLE | `evidence/TC-ST03-07-<product>.txt` |
| `TC-ST03-08` | Batch delete | Batch of keys is deleted; keys are absent afterwards; a batch containing an invalid key reports per-key outcome. | NOT AVAILABLE | `evidence/TC-ST03-08-<product>.txt` |
| `TC-ST03-09` | Object metadata | Custom metadata is stored and read back as separate headers; the `;` separator form is used. | NOT AVAILABLE | `evidence/TC-ST03-09-<product>.txt` |
| `TC-ST03-10` | Object tags | Tags are stored as a set using the `&` form; the AWS comma form and the space form are both recorded as they behave. | NOT AVAILABLE | `evidence/TC-ST03-10-<product>.txt` |
| `TC-ST03-11` | Bucket tags | Bucket tags are set, listed and removed independently of object tags. | NOT AVAILABLE | `evidence/TC-ST03-11-<product>.txt` |
| `TC-ST03-12` | Bucket policy | A policy granting and denying access is applied and is enforced; the denied request is captured. | NOT AVAILABLE | `evidence/TC-ST03-12-<product>.txt` |
| `TC-ST03-13` | IAM users, groups and policies | User and policy are created, attached, and effective; the credentials work and revocation takes effect. | NOT AVAILABLE | `evidence/TC-ST03-13-<product>.txt` |
| `TC-ST03-14` | Service accounts | A service account is created, used, and expiry is enforced. | NOT AVAILABLE | `evidence/TC-ST03-14-<product>.txt` |
| `TC-ST03-15` | STS | Assume-role returns temporary credentials that authenticate; expiry and scope are recorded. | NOT AVAILABLE | `evidence/TC-ST03-15-<product>.txt` |
| `TC-ST03-16` | Anonymous access | Anonymous listing is denied by default; with anonymous read enabled on one prefix, only that prefix is readable. | NOT AVAILABLE | `evidence/TC-ST03-16-<product>.txt` |
| `TC-ST03-17` | TLS | TLS connection succeeds and a plaintext connection to the TLS port is rejected; protocol and cipher recorded. | NOT AVAILABLE | `evidence/TC-ST03-17-<product>.txt` |
| `TC-ST03-18` | SSE-S3 | Object uploaded with SSE-S3 stores server-side; `mc stat` shows encryption applied. | NOT AVAILABLE | `evidence/TC-ST03-18-<product>.txt` |
| `TC-ST03-19` | SSE-C | Object uploaded with a customer key is readable with the same key and rejected with a different one. | NOT AVAILABLE | `evidence/TC-ST03-19-<product>.txt` |
| `TC-ST03-20` | Version enable, suspend and re-enable | Each transition is verified by behaviour, not by the API call returning success. | NOT AVAILABLE | `evidence/TC-ST03-20-<product>.txt` |
| `TC-ST03-21` | Multiple versions and delete markers | Suspended versioning creates delete markers; marker count and version list captured. | NOT AVAILABLE | `evidence/TC-ST03-21-<product>.txt` |
| `TC-ST03-22` | Restore a previous version | A prior version is retrieved and its content and checksum confirmed distinct from the current one. | NOT AVAILABLE | `evidence/TC-ST03-22-<product>.txt` |
| `TC-ST03-23` | Permanent version delete | A specific version is permanently removed and is then absent from the version listing. | NOT AVAILABLE | `evidence/TC-ST03-23-<product>.txt` |
| `TC-ST03-24` | Object lock governance | GOVERNANCE retention prevents deletion; bypass is possible only with the explicit privileged flag. | NOT AVAILABLE | `evidence/TC-ST03-24-<product>.txt` |
| `TC-ST03-25` | Object lock compliance | COMPLIANCE retention prevents deletion, and bucket removal is refused for the retention lifetime. | NOT AVAILABLE | `evidence/TC-ST03-25-<product>.txt` |
| `TC-ST03-26` | Retention extension and bypass | Extending retention succeeds; shortening it fails under COMPLIANCE. | NOT AVAILABLE | `evidence/TC-ST03-26-<product>.txt` |
| `TC-ST03-27` | Legal hold | Placing and releasing a legal hold prevents and then permits deletion. | NOT AVAILABLE | `evidence/TC-ST03-27-<product>.txt` |
| `TC-ST03-28` | Default retention | A bucket with default retention applies it to new objects without per-object configuration. | NOT AVAILABLE | `evidence/TC-ST03-28-<product>.txt` |
| `TC-ST03-29` | Lifecycle expiry, current and noncurrent | Expiry rules remove the right versions on schedule; the run is observed over time, not assumed. | NOT AVAILABLE | `evidence/TC-ST03-29-<product>.txt` |
| `TC-ST03-30` | Delete-marker cleanup | Expired delete markers are removed and the effect on visible listing is recorded. | NOT AVAILABLE | `evidence/TC-ST03-30-<product>.txt` |

### Commands

```bash
./tools/bin/lab up minio && ./tools/bin/lab up proxy
docker exec mc-client mc alias set minio http://lb-minio:80 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
# per-case: bucket, object and policy setup, then the operation under test,
# then the verification read-back that proves it (mc stat, mc cat --range,
# mc ls --versions). Every command's output is captured to evidence/.
docker exec mc-client mc ls --versions minio/<bucket>
docker exec mc-client mc stat minio/<bucket>/<key>
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
| `TC-ST03-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-09` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-10` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-11` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-12` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-13` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-14` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-15` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-16` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-17` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-18` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-19` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-20` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-21` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-22` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-23` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-24` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-25` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-26` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-27` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-28` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-29` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST03-30` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| All 30 functional cases executed with raw output captured | NOT AVAILABLE | — |
| Every PASS backed by a file under `evidence/` | NOT AVAILABLE | — |
| Object-lock cases confirm refusal rather than assuming it | NOT AVAILABLE | — |
| Metadata and tag forms measured, not inferred from documentation | NOT AVAILABLE | — |
| No case closed on the basis of a successful exit code alone | NOT AVAILABLE | — |

## Findings and Problems

* Object lock cannot be added to a bucket that already exists; the bucket must be
*   created with it. Already measured in ST02 finding 9.1.
* `mc cp --attr` separates metadata headers with `;`, and multiple object tags require `&`.
*   A comma form is rejected and a space form is accepted and silently stores one corrupted
*   tag. Already measured in ST02 findings 9.3 and 9.4. Re-confirmed here rather than assumed.
* A bucket holding a COMPLIANCE-locked object cannot be removed, even with
*   `mc rb --force --dangerous`, for the retention lifetime. Each case that needs a clean
*   bucket must therefore use a fresh name.
* The client images contain no `jq`, `awk`, `sed`, `grep` or `find`, so JSON Lines
*   cannot be parsed inside the client container. Parsing happens on the host.

## Limitations / Assumptions

**Assumptions.**
* The pinned MinIO build is the system under test and is not modified during the phase.
* Synthetic credentials are used throughout; no real credential is present in any evidence file.
* Object-lock lifecycle cases need the full retention period to elapse, so they are
*   scheduled with a short retention where the semantics under test permit it, and the
*   retention actually used is recorded per case.

**Limitations.**
* The host is below the reference configuration, so no result establishes reference-host performance.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. ST03 cannot be marked PASS or FAIL until every case above has run against the MinIO cluster with its raw output in `evidence/`.

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
