# MinIO vs Silo Evaluation

An evidence-backed comparison of the last open-source MinIO and Silo, covering
feature support, performance, and a go/no-go recommendation.

Upstream MinIO Community Edition has been archived and is no longer maintained.
Silo is a community fork intended as a drop-in replacement. This project exists to
establish, with reproducible evidence, whether that substitution is safe.

---

## Current state

**This project is not complete.** No phase is signed off. The laboratory and the
measurement tooling exist; the evaluation itself — feature validation, performance
benchmarking, the comparison and the recommendation — has not been performed.

| | |
|---|---|
| Phases complete | **0 of 11** |
| Partially evidenced, defects open | 2 (DEV-905, DEV-906) |
| Not started | 9 (DEV-907–DEV-915) |
| Epic DoD groups fully met | **0 of 7** |

The phase order is `DEV-905 → … → DEV-915`. Phases run in that order, and only
one heavy cluster runs at a time, so no result is a simultaneous two-product
measurement.

The prior `ST01`–`ST10` work is **not** treated as automatically complete under the
current contract. It is re-validated phase by phase, because the acceptance
criteria, the documentation structure and the execution environment have all changed.

## Phase status

| ID | Phase | Scope | Status | Report |
|---|---|---|---|---|
| DEV-905 | Repository, pinned versions, single-node lab, TLS, monitoring | Repository, version pinning, local machine assessment, MinIO single-node lab, TLS, basic monitoring, test matrix | Re-validation in progress | [docs/01](docs/01-repo-versions-and-lab/README.md) |
| DEV-906 | Test data and verification | Synthetic dataset, versioning/object-lock/lifecycle/IAM fixtures, manifest generation and comparison tooling | Partial — open defects | [docs/02](docs/02-test-data-and-verification/README.md) |
| DEV-907 | MinIO feature validation | MinIO single-node feature validation | Not started | [docs/03](docs/03-minio-feature-validation/README.md) |
| DEV-908 | MinIO distributed mode | Distributed mode, resilience, healing, expansion | Not started | [docs/04](docs/04-minio-distributed-mode/README.md) |
| DEV-909 | MinIO replication | Bucket/batch/site replication and runbook | Not started | [docs/05](docs/05-minio-replication/README.md) |
| DEV-910 | MinIO performance baseline | `warp` profiles and storage-layer `fio` measurements | Not started | [docs/06](docs/06-minio-performance-baseline/README.md) |
| DEV-911 | Silo functional validation | Silo functional validation in a comparable environment | Not started | [docs/07](docs/07-silo-functional-validation/README.md) |
| DEV-912 | Compatibility edge cases | Compatibility differences and O01–O08 | Not started | [docs/08](docs/08-compatibility-diff/README.md) |
| DEV-913 | Silo performance comparison | Identical benchmark methodology, side-by-side deltas | Not started | [docs/09](docs/09-silo-performance-comparison/README.md) |
| DEV-914 | Security and licensing | CVE review, provenance, licence review, maintenance risk, exit strategy | Not started | [docs/10](docs/10-security-licence-review/README.md) |
| DEV-915 | Evaluation and recommendation | Capability matrix, executive report, risks, final recommendation | Not started | [docs/11](docs/11-evaluation-report/README.md) |

Main epic: [DEV-904](https://github.com/atiqa-ai/minio-vs-silo-evaluation/issues/1).

## Execution environment

Results are produced on a VMware guest with 4 vCPU, ~7.7 GiB RAM and a single
48 GB filesystem. The reference host is 8 vCPU / 32 GiB, so this host is below
it on both CPU and memory. **Every performance result in this repository is
therefore indicative and none of it establishes reference-host performance.**

The gap is stated up front rather than discovered later, and it is recorded per
phase in that phase's environment section. Nothing in this repository claims the
reference configuration was met.

Every phase records: required specification, measured actual value, container
limits, the deviation and its reason, the effect on results, and the residual risk
to the conclusion. Two consequences are recorded up front rather than discovered
later:

- Performance numbers cannot support capacity or production-sizing conclusions.
- The dataset is smaller than the Profile B 5–10 GB floor, so the Profile B
  dataset requirement is **not met**. The measured value is always reported.

## Where to start

| If you want to… | Read |
|---|---|
| Know what has been done and what has not | This file, then [DEVIATIONS.md](DEVIATIONS.md) |
| See the full phase-by-phase plan and gates | [DEV-904-EXECUTION-PLAN.md](DEV-904-EXECUTION-PLAN.md) |
| Review the lab and the evidence so far | [docs/01](docs/01-repo-versions-and-lab/README.md) |
| Review the test data and verification | [docs/02](docs/02-test-data-and-verification/README.md) |
| Rebuild the lab from scratch | [docs/01](docs/01-repo-versions-and-lab/README.md) §12 |
| See every departure from the requirements | [DEVIATIONS.md](DEVIATIONS.md) |

## Repository layout

```text
.
├── README.md                     # This file: status and navigation
├── DEVIATIONS.md                 # Every departure from the requirements, with reasons
├── DEV-904-EXECUTION-PLAN.md     # Phase plan, gates, dependencies, risk register
├── docs/
│   ├── 01-repo-versions-and-lab/           # DEV-905
│   ├── 02-test-data-and-verification/      # DEV-906
│   ├── 03-minio-feature-validation/        # DEV-907
│   ├── 04-minio-distributed-mode/          # DEV-908
│   ├── 05-minio-replication/               # DEV-909
│   ├── 06-minio-performance-baseline/      # DEV-910
│   ├── 07-silo-functional-validation/      # DEV-911
│   ├── 08-compatibility-diff/              # DEV-912
│   ├── 09-silo-performance-comparison/     # DEV-913
│   ├── 10-security-licence-review/         # DEV-914
│   └── 11-evaluation-report/               # DEV-915
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
  scripts, the same commands. Only the storage backend varies between runs. In
  particular the *same* client drives both products, so a difference cannot be
  attributed to the client.
- **No mixed clusters.** MinIO and Silo nodes are never placed in the same
  cluster. Enforced by a pre-commit hook. Co-resident MinIO-only deployments are
  permitted where a phase genuinely needs them, such as replication, and are
  recorded as such.
- **Synthetic data only.** No real, company, or personal data is used anywhere.
- **Immutable image tags.** Every image is pinned by tag *and* registry digest,
  including `monitoring` and `warp`.
- **Evidence before conclusions.** No result is written from memory or inference;
  raw command output is captured first, and stale or unsupported evidence is
  corrected rather than cited.
- **Failures stay failures.** A finding that cannot be reproduced is reported as
  such, including findings about the lab itself.

## Known limitations worth knowing before reviewing

- **The host is below the reference profile**, and execution is in an approved
  controlled reduced-resource environment. Performance results are *indicative* and
  cannot support capacity conclusions (D-004, D-019).
- **Erasure coding doubles the disk footprint.** Four nodes with one drive each
  means a parity of two, so a 5.26 GiB dataset occupies roughly 11 GB on the
  volume. Capacity conclusions must be read in on-disk terms (D-016).
- **The dataset is below the Profile B floor.** Reduced dataset profiles are used
  so the phases are executable at all; the Profile B 5–10 GB requirement is recorded
  as not met, with the measured value (D-020).
- **The configured `warp` profile does not fit the disk.** The original parameters
  require more space than the host has, so benchmark parameters are reduced and the
  reduction is recorded (D-021).
- **Storage-layer tooling is being built, not assumed.** The containerised `fio`
  and NFS environments referenced by the requirements do not exist yet, so those
  cases are *not yet executable*, which is different from failed (D-010, D-018).
- **O01–O08 now have an authoritative source.** Earlier revisions recorded O05 and
  O08 as having no basis in the supplied requirements. The vendor publishes all
  eight compatibility conditions; they are captured as a documented vendor claim and
  then independently tested against both products (D-022).

## Repository security

This is a **public** repository and contains no credentials, internal hostnames,
domains, or addresses. `.env` files are excluded and only `.env.example`, holding
placeholders, is committed. `gitleaks` runs on every commit via a pre-commit hook,
and further hooks reject MinIO and Silo being mixed in one cluster and reject
environment claims the measurements do not support.

`DEV-904-project-documentation-pack/` is agent instruction material, not project
content, and is deliberately excluded from version control.

## Licence and attribution

This repository contains the evaluation's own scripts, Compose definitions and
documentation. MinIO, Silo, and `warp` are third-party projects under their own
licences; their images are referenced by tag and digest and are not redistributed
here.