# MinIO vs Silo Evaluation

**Evaluate the Last Open-Source MinIO and Silo, Feature by Feature**

## Project Status

| ID   | Jira          | Subtask                                                      | Status      | Required Output                             |
|------|---------------|--------------------------------------------------------------|-------------|---------------------------------------------|
| ST01 | DEV-905       | Set up repo, pin versions and build local Docker Compose lab | Complete   | Working local Compose lab                   |
| ST02 | DEV-906       | Seed test data and build verification toolkit                | In Progress | Synthetic data + manifest toolkit           |
| ST03 | DEV-907       | MinIO feature validation                                     | Not Started | MinIO feature baseline                      |
| ST04 | DEV-910       | MinIO performance baseline: local versus NFS-backed storage  | Not Started | MinIO performance baseline                  |
| ST05 | DEV-908/909   | MinIO distributed mode: resilience, healing and expansion    | Not Started | Distributed behavior + replication evidence |
| ST06 | DEV-911       | Silo functional validation                                   | Not Started | Silo functional results                     |
| ST07 | DEV-912       | S3 and client compatibility diff                             | Not Started | Compatibility comparison + O01–O08          |
| ST08 | DEV-913       | Benchmark Silo and compare with MinIO baseline               | Not Started | Performance comparison                      |
| ST09 | DEV-914       | Security, licensing, maintenance and CVE review              | Not Started | Security/licensing/maintenance review       |
| ST10 | DEV-915       | Capability matrix, evaluation report and recommendation      | Not Started | Final matrix + evaluation                   |

Main epic: [`DEV-904`](https://github.com/atiqa-ai/minio-vs-silo-evaluation/issues/1).
The **ST sequence is the execution order**; the Jira keys are a tracking map. See
`DEVIATIONS.md` D-012.

**Status values (use only these):** `Not Started` | `In Progress` | `Blocked` | `Complete`

## Quick Start

```bash
# Create the shared network
docker network create migration-net

# Follow docs/01-repository-and-lab/README.md for the rest
```

## Documentation Structure

```text
docs/
├── 00-srd/                          # Software Requirements Document
├── 00-test-cases/                   # All test cases
├── 00-evidence-guide/               # Evidence requirements
├── 00-guardrails/                   # Strict execution rules
├── 00-subtask-tracker/              # Subtask tracker + completion criteria
├── 01-repository-and-lab/           # ST01
├── 02-test-data-and-verification/   # ST02
├── 03-minio-feature-validation/     # ST03
├── 04-minio-performance-baseline/   # ST04
├── 05-minio-distributed-mode/       # ST05
├── 06-silo-functional-validation/   # ST06
├── 07-s3-client-compatibility/      # ST07
├── 08-silo-benchmark/               # ST08
├── 09-security-licensing-maintenance/ # ST09
└── 10-capability-matrix-evaluation/ # ST10
```

## Core Rules (Must Follow)

1. **MinIO is the baseline.** Always test MinIO first, then run the same test on Silo.
2. **Never mix MinIO and Silo nodes** in the same distributed cluster.
3. **Only synthetic data.** No real/company/personal data.
4. **Immutable image tags only** (`RELEASE.*`). Never use `latest`. Record digests.
5. **Evidence-first.** Every PASS/FAIL needs raw command output saved in `evidence/`.
6. **Local Docker Compose only.** No Kubernetes, cloud, VMs, or extra hosts.
7. **Do not expand scope.** Follow the SRD and guardrails strictly.
8. **Failures must stay failures.** Document them honestly.

## Final Recommendation Categories

At the end of ST10 the only allowed recommendations are:

- `Go`
- `No-Go`
- `Go-with-Conditions`

## Repository Security

This is a **public** repository. Never commit:

- Access keys, secret keys, passwords, tokens, private keys
- Internal IPs, hostnames, domains, email addresses
- Unredacted IAM or bucket metadata

Use placeholders such as `<ACCESS_KEY>`.
