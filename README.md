# MinIO vs Silo Evaluation

An evidence-backed comparison of the last open-source MinIO and Silo, covering
feature support, performance, and a go/no-go recommendation.

Upstream MinIO Community Edition has been archived and is no longer maintained.
Silo is a community fork intended as a drop-in replacement. This project exists to
establish, with reproducible evidence, whether that substitution is safe.

---

## Current state

**This project is not complete.** One of ten subtasks is finished and one is in
progress. None of the seven Epic-level Definition of Done groups is fully met.

| | |
|---|---|
| Subtasks complete | **1 of 10** (ST01) |
| In progress | 1 (ST02) |
| Not started | 8 (ST03–ST10) |
| Epic DoD groups fully met | **0 of 7** |
| SRD final outputs ready | **1 of 10** |

What exists today is the laboratory and the measurement tooling: two
four-node Docker Compose clusters, a monitoring stack, and a deterministic test
dataset with a manifest verification toolkit. The evaluation itself — feature
validation, performance benchmarking, the comparison and the recommendation —
has not been performed.

Reported honestly: eight of the ten subtask reports in `docs/` are structural
placeholders. They have the required headings and no findings behind them, because
their subtasks have not run.

## Subtask status

| ID | Jira | Subtask | Status | Report |
|---|---|---|---|---|
| ST01 | DEV-905 | Repository, pinned versions, local Compose lab | **Complete** | [docs/01](docs/01-repository-and-lab/README.md) |
| ST02 | DEV-906 | Test data and verification toolkit | **In Progress** | [docs/02](docs/02-test-data-and-verification/README.md) |
| ST03 | DEV-907 | MinIO feature validation | Not Started | [docs/03](docs/03-minio-feature-validation/README.md) |
| ST04 | DEV-910 | MinIO performance baseline | Not Started | [docs/04](docs/04-minio-performance-baseline/README.md) |
| ST05 | DEV-908/909 | MinIO distributed mode: resilience, healing, replication | Not Started | [docs/05](docs/05-minio-distributed-mode/README.md) |
| ST06 | DEV-911 | Silo functional validation | Not Started | [docs/06](docs/06-silo-functional-validation/README.md) |
| ST07 | DEV-912 | S3 and client compatibility differences | Not Started | [docs/07](docs/07-s3-client-compatibility/README.md) |
| ST08 | DEV-913 | Silo benchmark against the MinIO baseline | Not Started | [docs/08](docs/08-silo-benchmark/README.md) |
| ST09 | DEV-914 | Security, licensing, maintenance, CVE review | Not Started | [docs/09](docs/09-security-licensing-maintenance/README.md) |
| ST10 | DEV-915 | Capability matrix, evaluation and recommendation | Not Started | [docs/10](docs/10-capability-matrix-evaluation/README.md) |

Main epic: [DEV-904](https://github.com/atiqa-ai/minio-vs-silo-evaluation/issues/1).
The ST sequence is the execution order; the Jira keys are a tracking map, so
`DEV-907` runs before `DEV-908` (see `DEVIATIONS.md` D-012).

## Where to start

| If you want to… | Read |
|---|---|
| Know what has been done and what has not | This file, then [DEVIATIONS.md](DEVIATIONS.md) |
| Review the lab and the evidence so far | [docs/01](docs/01-repository-and-lab/README.md) |
| Review the test data and verification | [docs/02](docs/02-test-data-and-verification/README.md) |
| Rebuild the lab from scratch | [docs/01](docs/01-repository-and-lab/README.md) §12 |
| See every departure from the requirements | [DEVIATIONS.md](DEVIATIONS.md) |
| Read a structured status report | Generate it with `tools/bin/build-docx.py` |

## Repository layout

```text
.
├── README.md                 # This file: status and navigation
├── DEVIATIONS.md             # Every departure from the requirements, with reasons
├── docs/
│   ├── 01-repository-and-lab/            # ST01
│   ├── 02-test-data-and-verification/    # ST02
│   ├── 03-minio-feature-validation/      # ST03
│   ├── 04-minio-performance-baseline/    # ST04
│   ├── 05-minio-distributed-mode/        # ST05
│   ├── 06-silo-functional-validation/    # ST06
│   ├── 07-s3-client-compatibility/       # ST07
│   ├── 08-silo-benchmark/                # ST08
│   ├── 09-security-licensing-maintenance/ # ST09
│   └── 10-capability-matrix-evaluation/  # ST10
├── lab/
│   ├── compose/               # minio, silo, proxy, workload, monitoring
│   └── data/                  # cluster data and generated dataset (not committed)
└── tools/
    ├── bin/                   # lab, gen-dataset, seed-dataset, capture/verify-manifest
    └── build-minio.sh         # reproducible MinIO build
```

Each `docs/NN-*` folder holds a `README.md` report, an `evidence/` directory of raw
command output, and a `screenshots/` directory. Evidence files are the primary
record; every PASS claim in a report is backed by one.

## Method

The comparison is only meaningful if the two products are measured identically, so
the lab enforces that structurally:

- **MinIO first, then Silo.** The same dataset, the same client binary, the same
  scripts, the same commands. Only the storage backend varies between runs.
- **One product at a time.** Clusters are never co-resident on a shared disk, and
  MinIO and Silo nodes are never placed in the same cluster. Enforced by a
  pre-commit hook.
- **Synthetic data only.** No real, company, or personal data is used anywhere.
- **Immutable image tags.** Every image is pinned by tag *and* registry digest,
  including `monitoring` and `warp`.
- **Evidence before conclusions.** No result is written from memory or inference;
  raw command output is captured first, and stale or unsupported evidence is
  corrected rather than cited.
- **Failures stay failures.** A finding that cannot be reproduced is reported as
  such, including findings about the lab itself.

## Scope limits worth knowing before reviewing

- **Hardware is below the reference profile.** The host has 4 vCPU and ~7.7 GB
  RAM against a recommended 8 vCPU / 16 GB. Every performance number this project
  produces is therefore *indicative*, not authoritative (D-004).
- **Erasure coding doubles the disk footprint.** Four nodes with one drive each
  means a parity of two, so a 5.3 GiB dataset occupies roughly 11 GB on the
  volume. Capacity conclusions must be read in on-disk terms (D-016).
- **Some capability claims are not yet buildable.** The containerised `fio` and
  NFS tooling referenced by the requirements does not exist yet, so those cases
  are not yet executable — which is different from failed (D-010, D-018).
- **Two objectives cannot be assessed at all.** O05 and O08 have no basis in the
  supplied requirements, so no evidence could exist for them (D-006).

## Repository security

This is a **public** repository and contains no credentials, internal hostnames,
domains, or addresses. `.env` files are excluded and only `.env.example`, holding
placeholders, is committed. `gitleaks` runs on every commit via a pre-commit hook,
and a further hook rejects MinIO and Silo being mixed in one cluster.

## Licence and attribution

This repository contains the evaluation's own scripts, Compose definitions and
documentation. MinIO, Silo, and `warp` are third-party projects under their own
licences; their images are referenced by tag and digest and are not redistributed
here.