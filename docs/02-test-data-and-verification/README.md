# ST02 — Test Data and Verification Toolkit

**Status: In Progress**
**Jira:** `DEV-906`
**Epic:** `DEV-904`

---

## 1. Goal

Produce synthetic test data that is **byte-identical for both products**, and build the
verification toolkit that proves the data arrived intact on the server.

No data-integrity claim may rest on an operation merely having exited
successfully. Seven fields must be captured and checked:

```
Key | Version ID | Size | Checksum | Tags | Metadata | Retention
```

Two of them — **Version ID** and **Checksum** — can only be obtained from the server after
upload, so the manifest has two halves: a locally generated ground truth and a
server-captured copy that is compared against it.

Required test cases: `TC-ST02-01` … `TC-ST02-05` from the project test-case
specification, which is held externally and is not committed here.

---

## 2. Environment

Recorded `2026-10-01T19:48:12Z`, before the ST02 test runs below.

| Item | Value |
|---|---|
| Date (UTC) | 2026-10-01 |
| Docker Engine | 29.1.3 |
| Docker Compose | 2.40.3+ds1-0ubuntu1 |
| OS | Ubuntu 26.04.1 LTS |
| Kernel | Linux 7.0.0-31-generic x86_64 |
| Local machine | Intel(R) Core(TM) i5-8365U @ 1.60GHz, 4 vCPU, 7.7 GiB RAM |
| Virtualisation | `oracle` (VMware) — **inside the prohibited range**, see D-004 |
| Filesystem | ext4, 48 GB total, 15 GB available at ST02 start |
| cgroup | cgroup v2 |
| Topology | 4 nodes × 1 drive, one erasure pool, nginx load balancer, Profile B |

### Images

| Image | Digest (ID) |
|---|---|
| `minio-ce-local:RELEASE.2025-10-15T17-29-55Z` | `sha256:f71deba3825f2a57b4ab348b34aeec2fd1004c852f9d502f4d43dd17f7f4747a` |
| `pgsty/silo:RELEASE.2026-09-16T00-00-00Z` | `sha256:635197cb9f36d01bee221d34c1c7d7960f6a95c48b0b6c01d99cd13bdae51a46` |
| `mc-local:RELEASE.2025-08-13T08-35-41Z` | `sha256:80d58ab83508152a1410eefc8e7f1da25d5162140540429ee880732acfb382d2` |
| `minio/warp:v1.3.1` | `sha256:72ae1b02216b51bd102b73a6923b597c092a5acc7a655c936c2f31bee897a7c5` |

The MinIO and `mc` images are built from pinned upstream release tags because no pullable
image exists for them; the full source-to-image provenance chain is in
`docs/01-repo-versions-and-lab/evidence/minio-build-provenance.txt` and `DEVIATIONS.md` D-002,
D-003. Locally built images are pinned by immutable `RELEASE.*` tag and recorded image ID;
they have no registry digest.

### Client tooling

| Tool | Version | Commit |
|---|---|---|
| `mc` | `RELEASE.2025-08-13T08-35-41Z` | `7394ce0dd2a80935aded936b09fa12cbb3cb8096` |
| `mcli` | `RELEASE.2026-09-16T00-00-00Z` | `e952aa78f10a2b77dd525a2b7e3143bcda0cd377` |

`mcli` ships inside the Silo image at `/usr/bin/mcli`. `mc` is **also** present inside the
Silo image, which is what allows both products to be seeded by one identical script
(both products must use the same machine, topology, limits, storage, dataset
and benchmark parameters).

---

## 3. Prerequisites

* ST01 complete: `migration-net` exists, both Compose projects validate, `tools/bin/lab` works.
* Working directory `lab/data/dataset/` populated by `tools/bin/gen-dataset`.
* `.env` present with placeholder credentials. Never committed; real credentials
  may exist only in local ignored configuration.
* `workload` project running, so `mc-client` and `silo-client` exist.
* **Only one heavy cluster running at a time**.

---

## 4. Step-by-step procedure

### TC-ST02-01 — Seed synthetic test data

```bash
# One shared, deterministic dataset. Never copied between products.
tools/bin/gen-dataset

# Seed MinIO. The script creates a locked bucket, then for every object
# performs: upload -> tag set -> retention set.
tools/bin/seed-dataset minio eval-seed

# Tear MinIO down completely, bring Silo up, then seed the identical data.
tools/bin/lab down minio
tools/bin/lab up silo
tools/bin/seed-dataset silo eval-seed
```

### TC-ST02-02 — Generate the manifest

```bash
# Local ground truth: key, size, sha256, md5, tags, metadata, retention.
lab/data/dataset/dataset-manifest.jsonl

# Server capture: adds version ID, etag and the server's view of tags,
# metadata and retention.
tools/bin/capture-manifest minio eval-seed > evidence/manifest-minio.jsonl
```

### TC-ST02-03 — Verify data using the manifest toolkit

```bash
tools/bin/verify-manifest minio eval-seed lab/data/dataset/dataset-manifest.jsonl
```

Compares all seven required fields for every object and prints one line per mismatch.

### TC-ST02-04 — Cross-check with `mc diff`

```bash
docker exec mc-client mc diff /dataset minio/eval-seed
```

The comparison is bucket **against the local dataset directory**, not MinIO against Silo.
Running both heavy clusters simultaneously to diff them is not permitted, and diffing a
bucket against itself would prove nothing. A reader must be able to reproduce this
from a clean machine.

### TC-ST02-05 — Silo checksum verification

```bash
docker exec silo-client mcli checksum verify \
  --manifest manifest-silo.jsonl --report evidence/checksum-silo.jsonl
```

`mc` has **no** `checksum` command, so this cross-check exists for Silo only. That
asymmetry is itself a recorded client difference (ST07), not a skipped test.

---

## 5. Expected result

*Authored before the remaining ST02 runs, as each expected result must be written
before its test runs. Where an earlier exploratory
run has already happened, that is stated rather than presented as a prediction.*

| Test | Expected result |
|---|---|
| TC-ST02-01 | The generator produces byte-identical output on repeated runs. Every object uploads, is tagged and gets its retention applied; failure count 0. Silo's count equals MinIO's exactly. |
| TC-ST02-02 | The manifest holds all seven fields. Every object has a non-empty Version ID; no field is null or empty. |
| TC-ST02-03 | Zero mismatches across key, version ID presence, size, checksum, tags, metadata and retention for every object. |
| TC-ST02-04 | `mc diff` reports the bucket identical to the local dataset: only `NOTEMPTY`/`ONLYIN` differences expected, and zero of them. |
| TC-ST02-05 | `mcli checksum verify` reports every object matching, with zero mismatches, zero missing. |
| Both products | The MinIO and Silo manifests must agree field-for-field on key, size, tags, metadata and retention. Version ID and etag may differ, because those are server-assigned. |

**Expected result for the client-compatibility behaviours probed while building the
tooling** (these are already measured and are recorded in section 6, not predicted):

* `mc cp --attr` separates multiple metadata headers with `;`. A comma merges them into
  one header value.
* Multiple object tags require `&`. The AWS comma form errors; a space form is accepted
  and **silently** stored as one corrupted tag.
* Object lock cannot be added to an existing bucket; a bucket holding COMPLIANCE-locked
  objects cannot be deleted for the life of the retention period, not even with
  `mc rb --force --dangerous`.

---

## 6. Actual result

**Partial — ST02 is still In Progress.** Results are added here as evidence is captured,
with raw output in `evidence/`. Nothing is back-filled from memory.

### Work completed so far

| Item | Result | Evidence |
|---|---|---|
| `tools/bin/gen-dataset` exists and is deterministic | PASS — repeated runs produce identical bytes | section 8 |
| Dataset generated (first, 886 MB iteration) | PASS — 669 objects, 928844494 B | section 8 |
| `tools/bin/seed-dataset` created | PASS | `tools/bin/seed-dataset` |
| Smoke seed, 6 objects into `seed-smoke` | PASS — 6/6 upload+tag+retention | section 8 |
| Full 669-object seed into `eval-seed` | **INCOMPLETE** — aborted mid-run | section 8 |
| Object Lock on a 4-drive cluster | PASS | section 8 |
| `mc diff` cross-check | Not yet run | — |
| `mcli checksum verify` | Not yet run | — |
| Silo seeding | Not yet run | — |

The dataset is regenerated at the Profile B minimum of 5 GB before the final runs; the
886 MB figure above is the superseded first iteration.

---

## 7. PASS/FAIL

Not yet issued. ST02 cannot be marked PASS/FAIL until TC-ST02-01 … TC-ST02-05 have all
been executed against **both** products and their raw output is in `evidence/`.

---

## 8. Results table

Populated as each test completes. Every row is backed by raw command output in
`evidence/`, not by a retyped summary.

---

## 9. Findings and problems

Recorded in the order found. Failures and dead ends are kept, not deleted.

**9.1 — A whole investigation was run against a filesystem, not a server.**
An early attempt to reproduce an Object Lock failure used `mc` inside throwaway containers
whose `MC_CONFIG_DIR` was not persisted, and used alias names that had never been created.
`mc` does not error on an unresolvable alias: it silently falls back to a **filesystem
client**. Local directories were created under the container's `/work`, and the error
`SetObjectLockConfig is not supported for 'filesystem'` was read as a server capability
failure. The "buckets" involved never existed on either product. On the real `minio`
alias, Object Lock works first time. `tools/bin/seed-dataset` now aborts if the target
alias does not resolve to an `http(s)` endpoint, so this cannot recur silently.

**9.2 — Object lock: COMPLIANCE objects make a bucket permanently undeletable.**
`mc rb --force` removes a bucket holding GOVERNANCE-locked objects. A bucket holding a
COMPLIANCE-locked object cannot be removed even with `--force --dangerous`, for the life
of the retention period (30 days in this dataset). Each seeding run therefore needs a
fresh bucket name, or a cluster wipe. The seeder treats an existing bucket as a hard
error rather than half-seeding into it.

**9.3 — `mc` tag syntax differs from the AWS-documented form, and one form fails silently.**
Measured against the MinIO cluster with the same binary for both products:

| Input | Behaviour |
|---|---|
| `mc tag set ALIAS/B/K "a=1,b=2"` (AWS comma form) | hard error, `The TagValue you have provided is invalid` |
| `mc tag set ALIAS/B/K "a=1&b=2"` | **correct** — `{"tagset":{"a":"1","b":"2"}}` |
| `mc tag set ALIAS/B/K "a=1 b=2"` (space) | **accepted and silently corrupted** — `{"tagset":{"a":"1 b=2"}}` |
| `mc cp --tags "k=v"` | single tag only |
| `mc cp --tags k1=v1 --tags k2=v2` (repeated flag) | silently keeps only the **last** tag |

The space-separated form is the dangerous one: it exits 0 and stores a single tag whose
value contains `b=2`. An operator following this build's apparent syntax gets corrupted
data with no error. `mcli` uses `&` and also rejects the comma form, so the two clients
agree here — the AWS-documented comma syntax is wrong for both.

**9.4 — `mc cp --attr` uses `;`, not `,`.**

| Input | Stored as |
|---|---|
| `--attr "a=1,b=2"` | one header: `X-Amz-Meta-A: 1,b=2` |
| `--attr "a=1" --attr "b=2"` | only `X-Amz-Meta-B: 2` |
| `--attr "a=1;b=2"` | **correct** — two separate headers |

This was caught by reading the object back with `mc stat`, not by the upload succeeding.
It is exactly the failure mode the evidence-before-claim rule warns about.

**9.5 — The full seed was aborted mid-run.**
The 669-object seed into `eval-seed` was interrupted rather than allowed to finish. No
evidence of a completed full seed is claimed. The dataset is being regenerated at 5 GB
and the run repeated from a clean cluster.

**9.6 — The client images have no `jq`, `awk`, `sed`, `grep` or `find`.**
Both `mc-client` (UBI micro) and `silo-client` (distroless-style Silo base) provide only
bash builtins and a handful of coreutils. Manifest JSON cannot be parsed inside the
container. The toolkit therefore converts JSON Lines to tab-separated text on the host and
the container reads plain text, and the upload concurrency pool is built from bash job
control (`wait -n`) instead of `xargs -P`.

**9.7 — Sequencing slip, recorded for honesty.**
This subtask had already reached seeding data while its status still read `Not Started`
and while this README did not exist. The project rules require the status to be
set before work begins, and the expected result to be written before the test
runs. The status was corrected and this README authored before the
remaining ST02 runs; the exploratory work in 9.1–9.4 happened in that earlier window and
is reported as measured behaviour rather than as a prediction.

---

## 10. Conclusion

Deferred until TC-ST02-01 … TC-ST02-05 are complete for both products.

---

## 11. How to reproduce

```bash
git clone https://github.com/atiqa-ai/minio-vs-silo-evaluation.git
cd minio-vs-silo-evaluation

cp lab/compose/.env.example lab/compose/.env
# set synthetic credentials
./tools/bin/lab up workload

tools/bin/gen-dataset              # deterministic synthetic data
tools/bin/seed-dataset minio eval-seed

tools/bin/lab down minio           # only one heavy stack at a time
tools/bin/lab up silo
tools/bin/seed-dataset silo eval-seed
```

---

## 12. Cleanup

```bash
# Stop containers only. Safe: preserves cluster data.
tools/bin/lab down workload
tools/bin/lab down minio
tools/bin/lab down silo

# Destroy persistent data. DESTRUCTIVE - volumes must be gone before
# `down -v` is ever considered. Destructive commands require an explicit
# warning, and a dataset whose evidence is not yet captured is never destroyed.
#
# The MinIO/Silo bind mounts are written by root inside the containers, so
# they cannot be removed by the host user. Use a throwaway root container:
docker run --rm -v "$PWD/lab/data/minio:/d" <rootful-image> \
  bash -c 'rm -rf /d/* /d/.[!.]*'
```

`docker compose down -v` is **never** used while data must be preserved. A dataset
required by an active evidence set is never destroyed before its evidence is captured
and persisted.