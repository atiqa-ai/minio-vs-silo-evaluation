# Test Cases

## Test Case Structure

Every test must record:

* Test ID
* Objective
* Environment
* Prerequisites
* Exact command/procedure
* Expected result
* Actual result
* PASS/FAIL
* Evidence
* Findings

---

# ST01 — Repository and Lab

### TC-ST01-01

Verify Docker environment.

### TC-ST01-02

Verify Docker Compose v2.

### TC-ST01-03

Verify pinned MinIO image and digest.

### TC-ST01-04

Verify pinned Silo image and digest.

### TC-ST01-05

Verify `migration-net`.

### TC-ST01-06

Verify Compose projects and required connectivity.

### TC-ST01-07

Verify only required consoles/proxy publish ports.

### TC-ST01-08

Verify published ports bind to `127.0.0.1`.

---

# ST02 — Test Data and Verification

### TC-ST02-01

Seed synthetic test data.

### TC-ST02-02

Generate manifest containing:

* Key
* Version ID
* Size
* Checksum
* Tags
* Metadata
* Retention

### TC-ST02-03

Verify data using the manifest toolkit.

### TC-ST02-04

Cross-check using `mc diff`.

### TC-ST02-05

Verify Silo data using `mcli checksum verify`.

---

# ST03 — MinIO Feature Validation

### TC-ST03-01

Verify MinIO feature set.

### TC-ST03-02

Verify versioning.

### TC-ST03-03

Verify Object Lock.

### TC-ST03-04

Verify lifecycle behavior.

### TC-ST03-05

Record PASS/FAIL evidence for every feature.

---

# ST04 — MinIO Performance Baseline

### TC-ST04-01

Benchmark small-object PUT.

### TC-ST04-02

Benchmark small-object GET.

### TC-ST04-03

Benchmark DELETE.

### TC-ST04-04

Benchmark LIST.

### TC-ST04-05

Benchmark large-object PUT.

### TC-ST04-06

Benchmark large-object GET.

### TC-ST04-07

Benchmark mixed workload.

### TC-ST04-08

Benchmark multipart workload.

### TC-ST04-09

Benchmark versioned profile.

### TC-ST04-10

Measure local storage performance.

### TC-ST04-11

Measure NFS-backed storage performance.

### TC-ST04-12

Use `fio` to isolate raw storage-layer behavior.

### TC-ST04-13

Repeat benchmark runs and record noise.

---

# ST05 — MinIO Distributed Mode

### TC-ST05-01

Deploy MinIO distributed cluster.

### TC-ST05-02

Verify cluster state.

### TC-ST05-03

Test node failure/resilience.

### TC-ST05-04

Verify healing.

### TC-ST05-05

Test cluster expansion.

### TC-ST05-06

Test bucket replication.

### TC-ST05-07

Test batch replication.

### TC-ST05-08

Test site replication.

### TC-ST05-09

Record replication status/backlog.

---

# ST06 — Silo Functional Validation

### TC-ST06-01

Run corresponding MinIO feature tests on Silo.

### TC-ST06-02

Verify Silo versioning.

### TC-ST06-03

Verify Silo Object Lock.

### TC-ST06-04

Verify Silo lifecycle.

### TC-ST06-05

Validate Silo cluster behavior.

### TC-ST06-06

Validate Silo replication.

### TC-ST06-07

Validate resilience/healing where applicable.

### TC-ST06-08

Record Silo result beside corresponding MinIO result.

---

# ST07 — S3 and Client Compatibility

### TC-ST07-01

Compare S3 API behavior.

### TC-ST07-02

Compare client compatibility.

### TC-ST07-03

Check configuration compatibility.

### TC-ST07-04

Evaluate O01.

### TC-ST07-05

Evaluate O02.

### TC-ST07-06

Evaluate O03.

### TC-ST07-07

Evaluate O04.

### TC-ST07-08

Evaluate O05.

### TC-ST07-09

Evaluate O06.

### TC-ST07-10

Evaluate O07.

### TC-ST07-11

Evaluate O08.

### TC-ST07-12

Document applies/does-not-apply decision for every O01–O08 condition.

---

# ST08 — Silo Benchmark

### TC-ST08-01

Benchmark Silo small-object PUT.

### TC-ST08-02

Benchmark Silo small-object GET.

### TC-ST08-03

Benchmark Silo DELETE.

### TC-ST08-04

Benchmark Silo LIST.

### TC-ST08-05

Benchmark Silo large-object PUT.

### TC-ST08-06

Benchmark Silo large-object GET.

### TC-ST08-07

Benchmark Silo mixed workload.

### TC-ST08-08

Benchmark Silo multipart workload.

### TC-ST08-09

Benchmark Silo versioned profile.

### TC-ST08-10

Compare Silo results with MinIO baseline.

### TC-ST08-11

Ensure identical test conditions.

### TC-ST08-12

Categorize differences:

* Same
* Improved
* Degraded
* Broken

---

# ST09 — Security, Licensing, Maintenance and CVE Review

### TC-ST09-01

Review MinIO security position.

### TC-ST09-02

Review Silo security position.

### TC-ST09-03

Review relevant security advisories/CVEs.

### TC-ST09-04

Review MinIO licensing.

### TC-ST09-05

Review Silo licensing.

### TC-ST09-06

Review MinIO maintenance position.

### TC-ST09-07

Review Silo maintenance position.

### TC-ST09-08

Review Silo release cadence.

### TC-ST09-09

Document maintenance exit plan if Silo maintenance stops.

---

# ST10 — Final Evaluation

### TC-ST10-01

Build single capability matrix.

### TC-ST10-02

Compare all tested capabilities.

### TC-ST10-03

Verify all required evidence exists.

### TC-ST10-04

Verify O01–O08 decisions are documented.

### TC-ST10-05

Prepare final evaluation.

### TC-ST10-06

Prepare final recommendation:

```text
Go
No-Go
Go-with-Conditions
```
