# Subtask Tracker

| ID   | Subtask                                                      | Status      | Required Output                             |
| ---- | ------------------------------------------------------------ | ----------- | ------------------------------------------- |
| ST01 | Set up repo, pin versions and build local Docker Compose lab | Complete   | Working local Compose lab                   |
| ST02 | Seed test data and build verification toolkit                | Not Started | Synthetic data + manifest toolkit           |
| ST03 | MinIO feature validation                                     | Not Started | MinIO feature baseline                      |
| ST04 | MinIO performance baseline: local versus NFS-backed storage  | Not Started | MinIO performance baseline                  |
| ST05 | MinIO distributed mode: resilience, healing and expansion    | Not Started | Distributed behavior + replication evidence |
| ST06 | Silo functional validation                                   | Not Started | Silo functional results                     |
| ST07 | S3 and client compatibility diff                             | Not Started | Compatibility comparison + O01–O08          |
| ST08 | Benchmark Silo and compare with MinIO baseline               | Not Started | Performance comparison                      |
| ST09 | Security, licensing, maintenance and CVE review              | Not Started | Security/licensing/maintenance review       |
| ST10 | Capability matrix, evaluation report and recommendation      | Not Started | Final matrix + evaluation                   |

---

# Status Values

Use only:

```text
Not Started
In Progress
Blocked
Complete
```

---

# ST01

### Objective

Set up repository, pin versions and build the local Docker Compose lab.

### Completion Requirements

* [ ] Public repository created — **NOT MET**, see `DEVIATIONS.md` D-001 (local-only repository by request; Git history exists, no remote configured)
* [x] Docker environment ready — `docs/01-repository-and-lab/evidence/TC-ST01-01-minio.txt`
* [x] Docker Compose v2 ready — `evidence/TC-ST01-02-minio.txt`
* [x] MinIO version pinned — `RELEASE.2025-10-15T17-29-55Z`, `evidence/TC-ST01-03-minio.txt`
* [x] Silo version pinned — `RELEASE.2026-09-16T00-00-00Z`, `evidence/TC-ST01-04-silo.txt`
* [x] Image digests recorded — all five images, `evidence/TC-ST01-03-minio.txt` and `TC-ST01-04-silo.txt`
* [x] `migration-net` configured — `evidence/TC-ST01-05-{minio,silo}.txt`
* [x] Required Compose projects configured — `lab/compose/{minio,silo,proxy,workload}/compose.yml`, `evidence/TC-ST01-06-{minio,silo}.txt`
* [x] Required port exposure configured — `evidence/TC-ST01-07-{minio,silo}.txt`
* [x] Secret scanning/pre-commit scanning active — gitleaks 8.30.1 + `tools/bin/install-hooks`, `evidence/secret-scanning.txt`

### Evidence

* [x] Compose files — `lab/compose/`
* [x] Image digests — `evidence/minio-build-provenance.txt`, `TC-ST01-03-minio.txt`, `TC-ST01-04-silo.txt`
* [x] `docker compose ps` — `evidence/TC-ST01-06-{minio,silo}.txt`
* [x] Environment information — `evidence/TC-ST01-01-minio.txt`
* [x] Relevant command output — 16 test-case captures plus `secret-scanning.txt`

---

# ST02

### Objective

Seed synthetic data and build the verification toolkit.

### Completion Requirements

* [ ] Synthetic test data created
* [ ] Manifest toolkit created
* [ ] Manifest fields verified
* [ ] `mc diff` cross-check completed
* [ ] Silo checksum verification completed where applicable

### Evidence

* [ ] Raw outputs
* [ ] Manifest results
* [ ] Verification results

---

# ST03

### Objective

Establish MinIO functional baseline.

### Completion Requirements

* [ ] Feature set tested
* [ ] Versioning tested
* [ ] Object Lock tested
* [ ] Lifecycle tested
* [ ] PASS/FAIL recorded

### Evidence

* [ ] Commands
* [ ] Raw outputs
* [ ] Screenshots where useful
* [ ] Results table

---

# ST04

### Objective

Establish MinIO performance baseline.

### Completion Requirements

* [ ] Local storage tested
* [ ] NFS-backed storage tested
* [ ] Required `warp` workloads tested
* [ ] Repeated runs recorded
* [ ] Machine load recorded
* [ ] `fio` storage testing completed where required

### Evidence

* [ ] `warp` results
* [ ] `fio` results
* [ ] Repeated runs
* [ ] Machine-load information

---

# ST05

### Objective

Validate MinIO distributed behavior.

### Completion Requirements

* [ ] Distributed cluster running
* [ ] Resilience tested
* [ ] Healing tested
* [ ] Expansion tested
* [ ] Bucket replication tested
* [ ] Batch replication tested
* [ ] Site replication tested

### Evidence

* [ ] `mc admin info`
* [ ] Heal status
* [ ] Replication status/backlog
* [ ] Raw outputs
* [ ] Screenshots where useful

---

# ST06

### Objective

Run corresponding functional tests on Silo.

### Completion Requirements

* [ ] Features tested
* [ ] Versioning tested
* [ ] Object Lock tested
* [ ] Lifecycle tested
* [ ] Cluster behavior tested
* [ ] Replication tested
* [ ] Results placed beside MinIO results

---

# ST07

### Objective

Evaluate S3/client compatibility and O01–O08.

### Completion Requirements

* [ ] S3 behavior compared
* [ ] Client behavior compared
* [ ] Configuration compatibility checked
* [ ] O01 assessed
* [ ] O02 assessed
* [ ] O03 assessed
* [ ] O04 assessed
* [ ] O05 assessed
* [ ] O06 assessed
* [ ] O07 assessed
* [ ] O08 assessed
* [ ] Evidence-backed decision for every condition

---

# ST08

### Objective

Benchmark Silo against the MinIO baseline.

### Completion Requirements

* [ ] Same workloads used
* [ ] Same conditions used
* [ ] `warp` used
* [ ] Repeated runs recorded
* [ ] Results compared
* [ ] Differences categorized
* [ ] Severity recorded

---

# ST09

### Objective

Review security, licensing, maintenance and CVEs.

### Completion Requirements

* [ ] MinIO security reviewed
* [ ] Silo security reviewed
* [ ] Relevant CVEs/advisories reviewed
* [ ] MinIO license reviewed
* [ ] Silo license reviewed
* [ ] MinIO maintenance reviewed
* [ ] Silo maintenance reviewed
* [ ] Silo release cadence reviewed
* [ ] Exit plan documented

---

# ST10

### Objective

Produce the final capability matrix, evaluation and recommendation.

### Completion Requirements

* [ ] Capability matrix complete
* [ ] All required comparisons complete
* [ ] O01–O08 included
* [ ] Evidence checked
* [ ] Final evaluation written
* [ ] Recommendation written
* [ ] Repository status updated

---

# Overall Completion

Project status becomes **Complete** only when ST01–ST10 satisfy their required outputs and the final repository contains the required documentation and evidence.
