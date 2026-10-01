# Jira Project & Subtask Reference

> **Provenance.** Copied verbatim from the supplied project documentation
> (`Documentation/jira project & subtask reference.md`) on 2026-10-01. The
> document body is unmodified. What this repository does with it — the ST-to-Jira
> mapping, and the fact that the SRD execution order overrides the Jira key
> order — is documented in `docs/00-subtask-tracker/README.md` and
> `DEVIATIONS.md` D-012.

## Project Information

**Jira Project Key:** `DEV`

**Main Project / Epic:**
`DEV-904` — Evaluate the Last Open-Source MinIO and Silo, Feature by Feature

## Project Objective

Evaluate the last open-source MinIO release against Silo, a community-maintained MinIO fork, feature by feature through a local Docker Compose proof-of-concept.

The evaluation covers functional compatibility, distributed behavior, replication, performance, client compatibility, security, licensing, maintenance, CVEs, and the final capability assessment.

## Jira Subtasks

| Jira Key  | Subtask                                                                                 |
| --------- | --------------------------------------------------------------------------------------- |
| `DEV-905` | Set up the repo, pin versions and build the local Docker Compose lab                    |
| `DEV-906` | Seed test data and build the verification toolkit                                       |
| `DEV-907` | MinIO feature validation (single node), including versioning, object lock and lifecycle |
| `DEV-908` | MinIO distributed mode: resilience, healing and expansion                               |
| `DEV-909` | MinIO replication validation (bucket, batch and site) and replication runbook           |
| `DEV-910` | MinIO performance baseline: local versus NFS-backed storage                             |
| `DEV-911` | Silo functional validation (features, cluster, replication)                             |
| `DEV-912` | S3 and client compatibility diff (Silo versus last MinIO)                               |
| `DEV-913` | Benchmark Silo and compare with the MinIO baseline                                      |
| `DEV-914` | Security, licensing, maintenance and CVE review                                         |
| `DEV-915` | Capability matrix, evaluation report and recommendation                                 |

## Execution Sequence

The project should be executed in the following order:

`DEV-905`
→ `DEV-906`
→ `DEV-907`
→ `DEV-908`
→ `DEV-909`
→ `DEV-910`
→ `DEV-911`
→ `DEV-912`
→ `DEV-913`
→ `DEV-914`
→ `DEV-915`

## Jira Mapping

### Phase 1 — Environment and Test Preparation

**DEV-905**
Repository setup, version pinning, Docker Compose lab, networking, and environment preparation.

**DEV-906**
Synthetic test-data generation and verification tooling required for later comparisons.

### Phase 2 — MinIO Baseline

**DEV-907**
Validate MinIO single-node functionality, including:

* Basic S3 operations
* Versioning
* Object Lock
* Lifecycle

**DEV-908**
Validate MinIO distributed behavior:

* Resilience
* Failure handling
* Healing
* Cluster expansion

**DEV-909**
Validate MinIO replication:

* Bucket replication
* Batch replication
* Site replication
* Replication runbook

**DEV-910**
Establish the MinIO performance baseline:

* Local storage
* NFS-backed storage
* Comparable benchmark conditions

### Phase 3 — Silo Evaluation

**DEV-911**
Validate Silo functionality:

* Features
* Cluster behavior
* Replication

**DEV-912**
Compare Silo with the last open-source MinIO release for:

* S3 API compatibility
* Client compatibility
* Relevant behavioral differences

**DEV-913**
Benchmark Silo under conditions comparable to the MinIO baseline and document the results.

### Phase 4 — Risk and Final Evaluation

**DEV-914**
Review:

* Security
* Licensing
* Maintenance
* CVEs
* Long-term maintenance considerations

**DEV-915**
Produce the final:

* Capability matrix
* Feature-by-feature comparison
* Evaluation report
* Recommendation

## Jira Key Convention

The project uses the `DEV` Jira project key.

Examples:

* `DEV-904` → Main project/epic
* `DEV-905` → Repository and local lab subtask
* `DEV-906` → Test data and verification toolkit
* `DEV-907` → MinIO feature validation
* `DEV-908` → MinIO distributed mode
* `DEV-909` → MinIO replication
* `DEV-910` → MinIO performance baseline
* `DEV-911` → Silo functional validation
* `DEV-912` → Compatibility comparison
* `DEV-913` → Silo benchmarking
* `DEV-914` → Security/licensing/maintenance/CVE review
* `DEV-915` → Final evaluation and recommendation

## Documentation Rule

Jira issue keys should be used consistently in project documentation, GitHub issues/projects, subtask folders, commit messages, and progress reports where applicable.

Example commit format:

`DEV-905: set up local Docker Compose lab`

Example documentation reference:

`Jira: DEV-907`

## Project Structure

```text
DEV-904
│
├── DEV-905  Repository + Docker Compose Lab
├── DEV-906  Test Data + Verification Toolkit
├── DEV-907  MinIO Feature Validation
├── DEV-908  MinIO Distributed Mode
├── DEV-909  MinIO Replication
├── DEV-910  MinIO Performance Baseline
├── DEV-911  Silo Functional Validation
├── DEV-912  S3 + Client Compatibility
├── DEV-913  Silo Benchmarking
├── DEV-914  Security + Licensing + Maintenance + CVEs
└── DEV-915  Capability Matrix + Final Evaluation
```

## Scope Reference

This Jira structure represents the complete assigned project scope. The evaluation remains a **local Docker Compose proof-of-concept** and does not expand into Kubernetes, cloud deployment, production migration, or other storage alternatives unless explicitly required by the project scope.
