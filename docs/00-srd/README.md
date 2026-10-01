# Software Requirements Document (SRD)

## Project Title

**Evaluate the Last Open-Source MinIO and Silo, Feature by Feature**

---

## 1. Project Description

Upstream MinIO Community Edition is archived and read-only since **2026-04-25**, meaning it will receive no further releases or security patches.

**Silo** (`pgsty/silo`, image `docker.io/pgsty/silo`) is a community-maintained MinIO fork intended to serve as a near drop-in replacement.

The project will evaluate whether Silo is a suitable replacement for the last open-source MinIO by comparing:

* S3 API compatibility
* Configuration and monitoring compatibility
* On-disk format
* Features
* Versioning
* Object Lock
* Lifecycle
* Distributed cluster behavior
* Healing and resilience
* Replication
* Performance
* Client compatibility
* Security
* Licensing
* Maintenance

The evaluation must be based on **test evidence**, not assumptions about compatibility.

---

# 2. Project Objective

The objective is to build a local Docker Compose proof-of-concept and:

1. Establish a MinIO baseline.
2. Validate MinIO functionality and behavior.
3. Run the same tests against Silo.
4. Compare MinIO and Silo results under identical conditions.
5. Evaluate Silo's compatibility conditions **O01–O08**.
6. Benchmark Silo against the MinIO baseline.
7. Review security, licensing and maintenance.
8. Produce a capability matrix and final recommendation on whether Silo is a suitable replacement.

---

# 3. Project Scope

The project is a **local experiment**.

All infrastructure runs on the intern's own workstation or laptop using Docker Compose.

### The project does not use:

* Servers
* Virtual machines
* Cloud resources
* Kubernetes
* Nomad

All test data must be synthetic.

Results represent **lab-scale behavior**, not production capacity figures.

---

# 4. Environment Requirements

## 4.1 Infrastructure

The environment must use:

* Intern's workstation or laptop
* Docker Engine or Docker Desktop
* Docker Compose v2
* Local SSD storage

## 4.2 Orchestration

**Docker Compose only.**

No Kubernetes or Nomad.

## 4.3 Images

Images must:

* Use immutable `RELEASE.*` tags.
* Never use `latest`.
* Have their image digest recorded.

## 4.4 Networking

The environment uses one shared Docker network:

```text
migration-net
```

The network is created with:

```bash
docker network create migration-net
```

Compose projects are separated by component:

```text
minio-*
silo-*
proxy
workload
monitoring
```

Only consoles and the proxy publish ports, and published ports must be bound to:

```text
127.0.0.1
```

## 4.5 Comparable Conditions

MinIO and Silo must use identical:

* CPU limits
* Memory limits
* Volume types
* Test data
* Test profiles
* Repetition counts

Any Silo feature that does not work or cannot be verified must be documented rather than silently worked around.

---

# 5. Reference Test Environment

## Profile A — Recommended

| Requirement | Profile A                                    |
| ----------- | -------------------------------------------- |
| CPU         | 8+ cores                                     |
| RAM         | 32 GB                                        |
| Free SSD    | 200 GB                                       |
| Cluster     | 4 nodes × 2 drives + load-balancer container |
| Dataset     | 20–30 GB                                     |
| Coverage    | All subtasks                                 |

## Profile B — Fallback

| Requirement | Profile B                                   |
| ----------- | ------------------------------------------- |
| CPU         | 8 cores                                     |
| RAM         | 16 GB                                       |
| Free SSD    | 100 GB                                      |
| Cluster     | 4 nodes × 1 drive + load-balancer container |
| Dataset     | 5–10 GB                                     |
| Coverage    | All subtasks                                |

Benchmarks performed with reduced profiles must be labeled **indicative only**.

---

# 6. Storage Requirements

Storage uses a simple local mount:

* Docker volume, or
* Bind-mounted directory

The storage must be located on the local SSD.

Only one heavy stack should run at a time.

Machine load must be recorded during every benchmark.

---

# 7. Compatibility Requirements

Silo describes itself as a **conditional drop-in replacement** for upstream MinIO.

The project must evaluate all eight compatibility conditions:

```text
O01
O02
O03
O04
O05
O06
O07
O08
```

Each condition requires a written:

* Applies / Does-not-apply decision
* Supporting evidence

Special attention is required for:

* **O02** — custom authorization policy behavior
* **O03** — older authentication and notification settings
* **O04** — programs relying on old bugs
* **O06/O07** — multi-pool, replication and mixed-version behavior

In distributed mode:

* All nodes must run the same product.
* All nodes must run the same version.
* MinIO and Silo cannot be mixed within one cluster.

Compatibility must therefore be demonstrated **test by test**.

---

# 8. Performance and Verification Requirements

## 8.1 Performance Tool

`warp` must be used for every performance measurement.

Performance testing includes:

* Small-object PUT
* Small-object GET
* DELETE
* LIST
* Large-object PUT
* Large-object GET
* Mixed workloads
* Multipart operations
* Versioned profiles

## 8.2 Storage Performance

`fio` is used on the raw disk to isolate storage-layer bottlenecks from MinIO's own overhead.

## 8.3 Data Integrity

The manifest toolkit created in Subtask 2 must be used for data-integrity claims.

The manifest records:

* Key
* Version ID
* Size
* Checksum
* Tags
* Metadata
* Retention

Results must be cross-checked using:

```text
mc diff
```

For Silo:

```text
mcli checksum verify
```

---

# 9. Subtasks

## Subtask 1 — Set up repository, pin versions and build local Docker Compose lab

Requirements:

* Create the public GitHub repository.
* Set up the local Docker Compose environment.
* Pin image versions using immutable `RELEASE.*` tags.
* Record image digests.
* Create the required Compose structure.
* Create/use `migration-net`.
* Establish the local test environment.
* Enable secret scanning/pre-commit scanning.

The lab must be rebuildable from the repository.

---

## Subtask 2 — Seed test data and build verification toolkit

Requirements:

* Create synthetic test data.
* Build the manifest verification toolkit.
* Record key, version ID, size, checksum, tags, metadata and retention.
* Provide verification that can be reused for MinIO and Silo testing.

---

## Subtask 3 — MinIO feature validation

Establish the MinIO baseline.

Validate:

* Core feature set
* Versioning
* Object Lock
* Lifecycle

All results require PASS/FAIL evidence.

---

## Subtask 4 — MinIO performance baseline

Establish the MinIO performance baseline.

Test:

* Local storage
* NFS-backed storage

Performance measurements must use `warp`.

Storage-layer testing uses `fio` where required.

Repeated runs must be recorded so the noise level can be identified.

---

## Subtask 5 — MinIO distributed mode

Validate MinIO distributed behavior, including:

* Resilience
* Healing
* Expansion

Also validate:

* Replication

  * Bucket replication
  * Batch replication
  * Site replication

Required evidence includes relevant cluster information, healing status and replication status/backlog.

---

## Subtask 6 — Silo functional validation

Run the corresponding MinIO tests against Silo.

Validate:

* Features
* Cluster behavior
* Replication
* Versioning
* Object Lock
* Lifecycle
* Resilience/healing where applicable

Every Silo result must be recorded beside its corresponding MinIO result.

---

## Subtask 7 — S3 and client compatibility difference

Compare Silo with the last open-source MinIO for:

* S3 API behavior
* Client compatibility
* Configuration compatibility
* Relevant compatibility conditions

The compatibility assessment must include O01–O08 with written applies/does-not-apply decisions and evidence.

---

## Subtask 8 — Benchmark Silo and compare with MinIO baseline

Run the same performance tests against Silo.

Conditions must remain identical between MinIO and Silo.

Use:

```text
warp
```

for performance measurements.

Compare Silo results against the MinIO baseline.

Differences must be categorized as:

* Same
* Improved
* Degraded
* Broken

Each difference must have a severity.

---

## Subtask 9 — Security, licensing, maintenance and CVE review

Review both MinIO and Silo for:

### Security

Review relevant security information and advisories.

### Licensing

Review the applicable license.

Silo uses:

```text
AGPL-3.0
```

### Maintenance

Review:

* Maintenance model
* Release cadence
* SLA position
* Maintenance risk
* Exit plan if Silo maintenance stops

The review must be written for both options.

---

## Subtask 10 — Capability matrix, evaluation report and recommendation

Produce one capability matrix comparing MinIO and Silo.

The final evaluation must cover:

* Features
* Versioning
* Object Lock
* Lifecycle
* Distributed behavior
* Healing
* Replication
* Performance
* S3/client compatibility
* Security
* Licensing
* Maintenance
* O01–O08 compatibility conditions

The final report must provide a written recommendation:

```text
Go
No-Go
Go-with-Conditions
```

The recommendation must be supported by the collected evidence.

---

# 10. Documentation Requirements

Every subtask must have its own folder:

```text
docs/NN-name/
├── README.md
├── screenshots/
└── evidence/
```

Each README must contain:

1. Goal
2. Environment
3. Prerequisites
4. Step-by-step procedure
5. Expected result
6. Actual result
7. PASS/FAIL
8. Results table
9. Findings and problems
10. Conclusion
11. How to reproduce
12. Cleanup

Environment information must include:

* Image tags
* Image digests
* Docker version
* Compose version
* OS
* Local machine
* Topology
* Date

Commands must be exact and copy-pasteable.

---

# 11. Evidence Requirements

Every PASS or FAIL claim requires evidence.

Evidence must include:

* Raw command output saved as text
* Screenshots where useful
* Compose files
* `.env.example`
* `docker compose ps`
* Image digests
* Relevant logs
* `mc admin info`
* Heal status
* Replication status/backlog
* Exact benchmark commands
* Raw benchmark results
* Every repeated benchmark run

A screenshot alone is not sufficient evidence.

Failures and dead ends must remain documented.

---

# 12. Public Repository Requirements

Everything must be maintained in one public GitHub repository.

Suggested repository name:

```text
minio-vs-silo-evaluation
```

The GitHub Project should mirror the Jira subtasks.

Jira key must be included in issue titles.

Commits are made directly to:

```text
main
```

Commit messages should start with the subtask number, for example:

```text
ST05: add site replication steps
```

---

# 13. Repository Security Requirements

The public repository must contain **no sensitive or company-internal information**.

Do not commit:

* Access keys
* Secret keys
* Passwords
* Tokens
* Private keys
* Internal IPs
* Hostnames
* Domains
* Email addresses

Use placeholders such as:

```text
<ACCESS_KEY>
```

IAM and bucket-metadata exports must never be committed unredacted.

Screenshots must be checked before being pushed.

---

# 14. Epic-Level Definition of Done

The project is complete when:

### Local Lab

A working, documented Docker Compose lab exists and can be destroyed and rebuilt from the repository using:

```bash
docker compose up
```

The rebuild time is recorded.

### MinIO Baseline

The project contains recorded PASS/FAIL evidence for:

* Feature set
* Versioning
* Object Lock
* Lifecycle
* Distributed resilience
* Healing
* Bucket replication
* Batch replication
* Site replication
* `warp` performance
* Repeated-run noise

### Silo Comparison

The same tests have been executed on Silo.

Every Silo result appears next to the corresponding MinIO result.

Differences are categorized as:

* Same
* Improved
* Degraded
* Broken

Each difference has a severity.

O01–O08 each have an evidence-backed applies/does-not-apply decision.

### Performance

A `warp`-measured Silo vs MinIO performance comparison exists under identical conditions.

### Security and Maintenance

Security, licensing and maintenance reviews exist for both options, including an exit plan if Silo maintenance stops.

### Final Evaluation

A single capability matrix and written recommendation are provided.

### Repository

The public repository contains:

* Documentation
* Configurations
* Scripts
* Evidence

The README status table is current.

There must be no secrets or company-internal information in:

* Repository contents
* Git history
* Screenshots

---

# 15. Out of Scope

The following are explicitly outside this Epic:

* MinIO or Silo on an orchestrator other than Docker Compose
* MinIO → Silo data migration
* Replication-based migration
* Proxy cutover
* Rollback
* Kubernetes
* Other orchestrators
* Other alternatives such as Garage, SeaweedFS, RustFS or AIStor, except when mentioning them is necessary in the report
* Application code changes beyond SDK and endpoint configuration checks
* Second physical host
* Real network hardware
* Production storage
* Production-grade endpoint hardening beyond the TLS, authentication, encryption and exposure review in Subtask 10

---

# 16. Final Project Output

The final project must provide:

1. Rebuildable local Docker Compose lab
2. MinIO baseline
3. Silo functional validation
4. MinIO vs Silo feature comparison
5. Compatibility assessment for O01–O08
6. Client/S3 compatibility comparison
7. MinIO vs Silo performance comparison
8. Security, licensing and maintenance review
9. Capability matrix
10. Evidence-backed final recommendation
