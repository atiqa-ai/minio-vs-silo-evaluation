# ST09 — Security, Licensing, Maintenance and CVE Review

**Status:** Not Started
**Tracker:** `DEV-914`
**Epic:** `DEV-904`
**Legacy label:** ST09

> This is a pre-test plan. The phase has not been executed, so every result below
> reads `NOT AVAILABLE — phase not yet executed`. Expected results are written here
> **before** the runs, as required; actual results are filled in only from raw output
> in `evidence/`.

## Goal

Review both products' security posture, licensing, supply chain and project
health, so the final recommendation accounts for what happens after the
migration rather than only whether the benchmark looked good.

This phase is a review. It produces findings and citations, not measurements.

## Scope

In scope: known CVEs for the pinned versions, replication-related
advisories, licence terms, image provenance and signature verification,
TLS/authentication/encryption/exposure review, release cadence, maintainer and
project health, and a fallback or exit plan.

Out of scope: penetration testing, performance measurement, functional
validation, and the final recommendation itself.

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

* The exact pinned versions and digests from ST01, so advisories are checked against what actually runs.
* Both products' licence texts obtained from the pinned release, not from the current website.
* Image provenance available: the MinIO source-to-image chain recorded in ST01, and the Silo digest recorded there.
* Advisory sources identified and dated, so a review reflects a known point in time.
* The exposure surface enumerated from the actual running containers, not from documentation.

## Procedure and Evidence

Test cases from the project test inventory. Each row states the expected result
**before** execution; the observed result is recorded afterwards from raw output.

| Test case | Test | Expected result | Status | Evidence |
|---|---|---|---|---|
| `TC-ST09-01` | CVE review for pinned versions | Every advisory affecting the pinned version is listed with its identifier, severity and fixed version. | NOT AVAILABLE | `evidence/TC-ST09-01-<product>.txt` |
| `TC-ST09-02` | Replication-related advisories | Advisories affecting the replication path specifically, since replication is in scope for this migration. | NOT AVAILABLE | `evidence/TC-ST09-02-<product>.txt` |
| `TC-ST09-03` | Licence terms | Each product's licence read and its obligations recorded, including any restriction that affects this migration. | NOT AVAILABLE | `evidence/TC-ST09-03-<product>.txt` |
| `TC-ST09-04` | Image provenance | Each image traced to a verifiable source; the MinIO chain is already recorded in ST01. | NOT AVAILABLE | `evidence/TC-ST09-04-<product>.txt` |
| `TC-ST09-05` | Signatures and checksums | Each artefact's checksum and any available signature verified. | NOT AVAILABLE | `evidence/TC-ST09-05-<product>.txt` |
| `TC-ST09-06` | TLS configuration | TLS settings reviewed, with protocol versions and ciphers recorded for both products. | NOT AVAILABLE | `evidence/TC-ST09-06-<product>.txt` |
| `TC-ST09-07` | Authentication | Authentication mechanisms reviewed, including default credentials and root-user handling. | NOT AVAILABLE | `evidence/TC-ST09-07-<product>.txt` |
| `TC-ST09-08` | Encryption | Encryption at rest and in transit reviewed, including which keys are managed by the operator. | NOT AVAILABLE | `evidence/TC-ST09-08-<product>.txt` |
| `TC-ST09-09` | Network exposure | The real exposure surface enumerated from running containers and compared to the intended surface. | NOT AVAILABLE | `evidence/TC-ST09-09-<product>.txt` |
| `TC-ST09-10` | Release cadence | Observed release cadence for both projects, with dates, not impressions. | NOT AVAILABLE | `evidence/TC-ST09-10-<product>.txt` |
| `TC-ST09-11` | Maintainer and project health | Bus-factor signals, issue responsiveness and governance recorded with sources. | NOT AVAILABLE | `evidence/TC-ST09-11-<product>.txt` |
| `TC-ST09-12` | Fallback and exit plan | A written fallback path exists, including what a reversal would cost in time and re-replication. | NOT AVAILABLE | `evidence/TC-ST09-12-<product>.txt` |
| `TC-ST09-13` | Secret scanning confirmed active | Secret scanning is installed and demonstrated to reject a commit containing a credential. | NOT AVAILABLE | `evidence/TC-ST09-13-<product>.txt` |

### Commands

```bash
# Exposure surface from what is actually running, not from documentation
docker compose -f lab/compose/minio/compose.yml ps --format '{{.Name}} {{.Ports}}'
docker compose -f lab/compose/silo/compose.yml  ps --format '{{.Name}} {{.Ports}}'

# Secret scanning must be demonstrated to reject, not merely to be installed
./tools/bin/install-hooks
# then: add a credential to a scratch file and confirm the commit is refused

# Supply chain
docker image inspect --format '{{index .RepoDigests 0}}' pgsty/silo:RELEASE.2026-09-16T00-00-00Z
sha256sum lab/images/minio/  # compare against the provenance file recorded in ST01
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
| `TC-ST09-01` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-02` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-03` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-04` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-05` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-06` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-07` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-08` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-09` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-10` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-11` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-12` | NOT AVAILABLE | NOT AVAILABLE | — |
| `TC-ST09-13` | NOT AVAILABLE | NOT AVAILABLE | — |

## Acceptance Criteria

| Criterion | Status | Evidence |
|---|---|---|
| Every advisory affecting the pinned versions listed and dated | NOT AVAILABLE | — |
| Licence obligations recorded for both products | NOT AVAILABLE | — |
| Image provenance and checksums verified | NOT AVAILABLE | — |
| Exposure surface enumerated from running containers | NOT AVAILABLE | — |
| Secret scanning demonstrated to reject a real credential | NOT AVAILABLE | — |
| A fallback and exit plan exists in writing, with its cost stated | NOT AVAILABLE | — |

## Findings and Problems

* No Jira instance or credentials are available in this environment, so the review cannot
*   link to tracker records. Tracker keys are carried in commit messages and issue bodies
*   instead, which is greppable, and the absence of a live link is recorded as a gap.
* The repository was made public on 2026-10-01. Before that date it was deliberately
*   not public, so any secret-scanning evidence captured earlier predates the final
*   exposure surface and is re-run once the repository is public.

## Limitations / Assumptions

**Assumptions.**
* Advisory data reflects the sources as read on the review date, which is recorded per finding.
* Licence conclusions are based on the pinned release's licence text, not on a current marketing page.
* Provenance claims rest on the artefacts actually present in this repository, not on vendor statements.

**Limitations.**
* The host is below the reference configuration, so a document review cannot establish the absence of a vulnerability, only the absence of a known one at the pinned version.
* Only one heavy cluster runs at a time, so no result is a MinIO-versus-Silo
  measurement taken simultaneously; products are compared in separate passes under
  identical parameters.

## Conclusion

Deferred. ST09 cannot be marked PASS or FAIL until the review is complete, cited, and a fallback plan exists in writing.

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
