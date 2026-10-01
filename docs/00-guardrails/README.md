# Restricted Safeguards & Project Execution Guardrails

## Project

**Evaluate the Last Open-Source MinIO and Silo, Feature by Feature**

---

## 1. Primary Rule

The model must complete the project **strictly according to the approved SRD and project requirements**.

The model must not:

* Add new project requirements.
* Expand the project scope.
* Introduce unrelated technologies.
* Change the project's testing methodology without a documented requirement.
* Replace project-defined tools with alternative tools without a requirement.
* Turn general DevOps best practices into project deliverables.
* Assume a feature is compatible without testing and evidence.

If something is not required by the SRD/project, it must **not become a project requirement**.

---

# 2. Environment Restriction

The project is a **local Docker Compose proof of concept**.

The model must keep the project within:

```text
Intern workstation/laptop
        ↓
Docker Engine / Docker Desktop
        ↓
Docker Compose v2
        ↓
MinIO / Silo test environments
```

### Strictly prohibited as project infrastructure

Do not introduce:

* AWS
* Azure
* Google Cloud
* EC2
* Cloud S3
* Kubernetes
* Nomad
* Production servers
* Virtual machines
* Second physical hosts
* Real network hardware

These are outside the project scope.

---

# 3. Orchestration Restriction

The only orchestrator permitted is:

```text
Docker Compose
```

Do not redesign the project around:

```text
Kubernetes
Nomad
Docker Swarm
Terraform
Ansible
Helm
```

unless the project requirements themselves are explicitly changed.

---

# 4. MinIO/Silo Isolation Rule

**MinIO and Silo must never be mixed inside the same cluster.**

A MinIO cluster contains MinIO nodes.

A Silo cluster contains Silo nodes.

Do not create:

```text
MinIO node
      +
Silo node
      +
MinIO node
```

as one distributed cluster.

Every cluster must use the same:

* Product
* Version

The MinIO and Silo environments are compared **independently**.

---

# 5. Baseline Rule

**MinIO is the baseline.**

The workflow must remain:

```text
MinIO
  ↓
Establish baseline
  ↓
Record evidence
  ↓
Run same test on Silo
  ↓
Compare results
```

The model must not evaluate Silo in isolation.

Every relevant Silo test should have a corresponding MinIO result.

---

# 6. Identical-Test Rule

Where the project requires comparison, the test performed on Silo must correspond to the MinIO test.

Do not:

* Change the workload only for Silo.
* Use different test data.
* Use different resource limits.
* Use different repetition counts.
* Change the test conditions to make results easier to obtain.
* Silently skip a failed Silo feature.

Required comparison conditions include identical:

* CPU limits
* Memory limits
* Volume types
* Data
* Profiles
* Repetition counts

---

# 7. Synthetic Data Only

Only synthetic test data may be used.

Never introduce:

* Company data
* Personal data
* Production data
* Real credentials
* Internal datasets
* Confidential files

The project is a lab experiment.

---

# 8. Version Pinning Safeguard

Images must use immutable:

```text
RELEASE.*
```

tags.

Never use:

```text
latest
```

Image digests must be recorded.

The model must not silently change the tested versions during the project.

If a version changes, the environment and evidence must reflect the new version.

---

# 9. Performance Testing Safeguard

All performance numbers for this project must use:

```text
warp
```

Do not replace `warp` with arbitrary shell loops or another benchmark tool for the project's official performance numbers.

Performance testing may include:

* Small-object PUT
* Small-object GET
* DELETE
* LIST
* Large-object PUT
* Large-object GET
* Mixed workloads
* Multipart
* Versioned profiles

`fio` is used where required to isolate raw storage-layer bottlenecks.

---

# 10. Data Integrity Safeguard

Data-integrity claims must use the verification methodology defined by the project.

Use the manifest toolkit from Subtask 2.

Verification includes:

* Key
* Version ID
* Size
* Checksum
* Tags
* Metadata
* Retention

Cross-check with:

```text
mc diff
```

and for Silo:

```text
mcli checksum verify
```

The model must not claim that data is correct merely because an operation completed successfully.

---

# 11. Evidence-First Rule

No important result may be presented as a fact without evidence.

For every PASS/FAIL:

```text
Test
 ↓
Expected result
 ↓
Command
 ↓
Actual result
 ↓
Raw output
 ↓
PASS/FAIL
 ↓
Conclusion
```

A screenshot alone is not sufficient.

Raw command output must be retained in the evidence directory.

---

# 12. No Silent Workarounds

If a Silo feature:

* Does not work, or
* Cannot be verified,

the model must **document the limitation**.

It must not silently:

* Change the test.
* Modify the requirement.
* Ignore the failure.
* Replace the feature with another feature.
* Hide the failure.
* Declare compatibility without evidence.

The project explicitly requires such cases to be documented rather than silently worked around.

---

# 13. Compatibility Safeguard

The model must not use the phrase:

> "Silo is a drop-in replacement."

as an unsupported conclusion.

Silo's compatibility is **conditional** and must be evaluated through O01–O08.

For each condition:

```text
Condition
↓
Does it apply?
↓
Evidence
↓
Applies / Does-not-apply
↓
Impact
```

No compatibility condition may be skipped.

---

# 14. Special Compatibility Areas

The model must specifically preserve attention to:

### O02

Custom authorization policy behavior.

### O03

Older authentication and notification settings.

### O04

Programs relying on old bugs.

### O06/O07

Multi-pool, replication and mixed-version behavior.

These must receive written evidence-backed decisions.

---

# 15. Resource Safeguard

Running distributed storage, monitoring and benchmarking workloads on one machine is resource intensive.

Therefore:

* MinIO and Silo must use comparable resource limits.
* Heavy stacks must run one at a time.
* Machine load must be recorded during benchmarks.

Do not run multiple heavy experimental stacks simultaneously just to speed up the project.

---

# 16. Volume Destruction Safeguard

The model must treat this command as destructive:

```bash
docker compose down -v
```

It removes Docker volumes.

Therefore:

**Never recommend or execute `docker compose down -v` when the stack contains data that must be preserved.**

Cleanup instructions must distinguish between:

```text
Stop/remove containers
```

and:

```text
Destroy persistent volumes
```

---

# 17. Repository Safeguard

All project documentation, configurations, scripts and evidence must remain within the project repository structure.

Each subtask uses:

```text
docs/NN-name/
├── README.md
├── screenshots/
└── evidence/
```

The model must not create unrelated project documentation structures unless required by the project.

---

# 18. Documentation Safeguard

Every subtask documentation must contain:

1. Goal
2. Environment
3. Prerequisites
4. Exact procedure
5. Expected result
6. Actual result
7. PASS/FAIL
8. Results table
9. Findings and problems
10. Conclusion
11. Reproduction
12. Cleanup

The expected result must be written **before** running the test.

The actual result must reflect what actually happened.

---

# 19. Failure Honesty Rule

Failures must remain failures.

The model must never:

* Convert FAIL into PASS.
* Hide failed tests.
* Delete evidence of failed tests.
* Rewrite the expected result after seeing the actual result.
* Claim success because a workaround produced a different result.

Dead ends and failures remain documented.

---

# 20. Public Repository Security Safeguard

The repository is public.

Never commit:

* Access keys
* Secret keys
* Passwords
* Tokens
* Private keys
* Internal IP addresses
* Internal hostnames
* Internal domains
* Email addresses
* Unredacted IAM exports
* Unredacted bucket metadata

Use placeholders such as:

```text
<ACCESS_KEY>
```

Screenshots must also be checked for sensitive information before being committed.

---

# 21. Scope-Expansion Safeguard

The model must reject scope expansion during execution.

The following must **not** become additional project tasks:

* CI/CD pipelines
* Terraform infrastructure
* AWS deployment
* Kubernetes deployment
* Production deployment
* Production migration
* Proxy cutover
* Rollback implementation
* Application redesign
* Additional storage platforms as alternatives
* Production hardening beyond the defined security review

These are outside the approved project scope.

---

# 22. No Unrequested Tool Expansion

Use the tools specifically defined by the project where applicable:

```text
Docker Compose
mc
mcli
warp
fio
Manifest toolkit
```

The model must not turn additional tools into mandatory project dependencies merely because they are commonly used in DevOps.

If another tool becomes necessary for a specific implementation step, it must remain an implementation detail rather than becoming a new project requirement.

---

# 23. No Production Claims

This project is a local proof of concept.

Therefore, the model must not describe lab results as:

* Production capacity
* Production SLA
* Production reliability
* Production performance
* Guaranteed compatibility
* Guaranteed migration safety

Results must be described as **lab-scale experimental evidence**.

---

# 24. No Assumption-Based Conclusions

The model must distinguish:

```text
Documented fact
Test result
Observed behavior
Interpretation
Final evaluation
```

For example:

```text
Silo claims compatibility
        ≠
Compatibility has been proven
```

Compatibility is only supported where the project's tests and evidence demonstrate it.

---

# 25. Final Comparison Safeguard

The final capability matrix must be based on actual project evidence.

Differences must be categorized only as:

```text
Same
Improved
Degraded
Broken
```

with severity where required.

The model must not invent a difference where the evidence shows no difference.

It must also not hide a difference because it makes the final recommendation less favorable.

---

# 26. Recommendation Safeguard

The final recommendation must be produced **after** the evidence and capability matrix are complete.

The allowed project recommendation categories are:

```text
Go
No-Go
Go-with-Conditions
```

The model must support the recommendation with the documented comparison and evidence.

---

# 27. Project Completion Gate

The model must consider the project complete only when the SRD's required outputs exist:

```text
Local Docker Compose Lab
        ↓
MinIO Baseline
        ↓
MinIO Feature/Cluster/Replication Tests
        ↓
Silo Functional Validation
        ↓
Client/S3 Compatibility
        ↓
O01–O08 Assessment
        ↓
Performance Comparison
        ↓
Security/Licensing/Maintenance Review
        ↓
Capability Matrix
        ↓
Final Evaluation & Recommendation
        ↓
Complete Evidence Repository
```

No required stage may be skipped merely to finish the project faster.

---

# 28. Model Operating Rule

For every future task related to this project, the model must ask internally:

### 1. Is this required by the approved SRD?

If **yes**, proceed.

If **no**, do not turn it into a project requirement.

### 2. Is it inside the defined scope?

If **yes**, proceed.

If **no**, do not implement it as part of this project.

### 3. Is there evidence?

If **yes**, report the result.

If **no**, do not present the claim as verified.

### 4. Does it preserve the MinIO → Silo comparison?

If **yes**, proceed.

If **no**, do not alter the comparison methodology.

### 5. Does it preserve the local Docker Compose environment?

If **yes**, proceed.

If **no**, it is outside the project unless the SRD is formally changed.

---

# 29. Highest-Priority Rule

When there is a conflict between:

* General DevOps best practice
* Model suggestion
* Common industry approach
* A new technology
* A convenient shortcut

and the **approved project SRD**,

the **approved project SRD takes priority**.

The model must complete this project **according to the defined requirements, not according to what it thinks would make the project broader or more advanced.**
