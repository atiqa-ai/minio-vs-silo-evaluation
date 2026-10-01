# Evidence Guide

## 1. Purpose

Every project result must be supported by evidence.

A screenshot alone is not sufficient for PASS/FAIL claims.

---

# 2. Required Evidence Structure

Each subtask:

```text
docs/NN-name/
├── README.md
├── screenshots/
└── evidence/
```

---

# 3. Required README Sections

Every subtask README must contain:

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

---

# 4. Environment Evidence

Record:

* Image tag
* Image digest
* Docker version
* Compose version
* OS
* Local machine
* Topology
* Date

---

# 5. Command Evidence

For every important test:

```text
Command
↓
Expected result
↓
Actual command output
↓
PASS/FAIL
```

Save raw command output as text inside `evidence/`.

---

# 6. Cluster Evidence

Where applicable, retain:

```text
docker compose ps
mc admin info
heal status
replication status
replication backlog
relevant logs
```

---

# 7. Performance Evidence

For every benchmark retain:

* Exact benchmark command
* Workload/profile
* MinIO/Silo version
* Image digest
* Test conditions
* Raw `warp` result
* Every repeated run
* Machine load
* Comparison result

Do not retain only a final number.

---

# 8. Storage Evidence

Where storage behavior is being isolated, retain:

* Exact `fio` command
* Raw `fio` output
* Storage configuration
* Corresponding MinIO/Silo benchmark information where applicable

---

# 9. Data Integrity Evidence

For data-integrity claims retain:

* Manifest results
* Key
* Version ID
* Size
* Checksum
* Tags
* Metadata
* Retention
* `mc diff` output
* `mcli checksum verify` output for Silo

---

# 10. Compatibility Evidence

For every O01–O08:

```text
Condition
↓
Test/assessment
↓
Expected result
↓
Actual result
↓
Evidence
↓
Applies / Does-not-apply
```

No compatibility condition is considered assessed without supporting evidence.

---

# 11. MinIO vs Silo Evidence

Where a test is comparative:

```text
MinIO Result
+
MinIO Evidence
        ↓
Silo Result
+
Silo Evidence
        ↓
Comparison
```

Both sides must be retained.

---

# 12. Failure Evidence

If a test fails:

* Save the raw output.
* Record the actual behavior.
* Keep the failure in the README.
* Document the problem.
* Do not silently work around it.
* Do not remove the evidence.

If a feature cannot be verified, document that explicitly.

---

# 13. Screenshot Rules

Screenshots are supporting evidence.

Use screenshots where useful.

Before committing screenshots to the public repository, check that they contain no:

* Access keys
* Secret keys
* Passwords
* Tokens
* Private keys
* Internal IPs
* Internal hostnames
* Internal domains
* Email addresses
* Sensitive IAM information
* Sensitive bucket metadata
* Company-internal information

---

# 14. Repository Evidence

The repository must retain:

* Compose files
* `.env.example`
* `docker compose ps`
* Image digests
* Relevant logs
* Required command outputs
* Benchmark results
* Screenshots where useful

---

# 15. Reproducibility

Documentation must be detailed enough that a person who was not involved in the test can follow it from a clean machine and obtain the same result.

Exact copy-pasteable commands must be provided.

Failures and dead ends must remain documented.

---

# 16. Evidence Completion Rule

A subtask is not considered complete merely because the command worked.

It is complete when:

```text
Test performed
      ↓
Expected result recorded
      ↓
Actual result recorded
      ↓
Raw evidence saved
      ↓
PASS/FAIL recorded
      ↓
Findings documented
      ↓
Conclusion documented
```
