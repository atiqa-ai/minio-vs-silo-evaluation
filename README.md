# MinIO vs Silo Evaluation

An evidence-backed comparison of the last open-source MinIO and Silo, covering
feature support, performance, and a go/no-go recommendation.

Upstream MinIO Community Edition has been archived and is no longer maintained.
Silo is a community fork intended as a drop-in replacement. This project exists to
establish, with reproducible evidence, whether that substitution is safe.

---

## Current state

**No phase has been executed or signed off.** The plans, the laboratory and the
measurement tooling now exist and are verified; the measurements themselves have
not been taken.

| | |
|---|---|
| Phases with a complete, reviewable pre-test plan | **11 of 11** |
| Phases executed and signed off | **0 of 11** |
| Test cases specified | **175** |
| Phases with raw evidence captured | 2 (DEV-905, DEV-906) |
| Open defects | 3 (R7, R13, NFS client mount) |
| Epic DoD groups fully met | **0 of 7** |

Every phase document carries all 14 required sections and its own test cases with
expected results, so the phase can be executed without further design work. That
is the current milestone: **the plan is finished, the run has not started.**

The phase order is `DEV-905 → … → DEV-915`. Phases run in that order, and only
one heavy cluster runs at a time, so no result is a simultaneous two-product
measurement.

### Recent work

- **Replication target added.** `docs/05` documented commands against
  `lab/compose/replication-target/compose.yml`, which did not exist — DEV-909 was
  not executable. It now exists as a real project: four MinIO nodes
  `rep-minio-1..4`, its own credentials, no published ports. `capture-manifest`
  and `verify-manifest` accept `rep`, which they previously did not, so the
  target's manifest can be checked at all.
- **Unresolvable citations removed throughout the code and configuration**, not
  just in Markdown. Compose files, Dockerfiles and `tools/bin/` scripts cited
  guardrails and SRD sections that do not exist. Most consequentially, about a
  dozen comments across five Compose files attributed the lab's port policy to a
  subsection that does not exist; **the specification says nothing about ports
  anywhere**. The practice is unchanged and still sensible, but it is now recorded
  as a lab decision rather than as a requirement.
- **Mixed-cluster check now discovers its own inputs** instead of listing files,
  so a cluster added later cannot escape the check by not being named.
- **Containerised storage tooling built.** `fio-local:3.41-r0` and
  `nfs-local:2.6.4-r6` exist, and `lab/compose/storage/` wires them in. This
  supersedes the older "not yet executable" wording in D-010 and D-018, which
  described a state that no longer holds.
- **All 12 GitHub issue bodies repaired**, and the full commit history scanned for
  secrets: 30 commits, no leaks.

## Phase status

| ID | Phase | Scope | Plan | Execution | Report |
|---|---|---|---|---|---|
| DEV-905 | Repository, pinned versions, single-node lab, TLS, monitoring | Repository, version pinning, local machine assessment, MinIO single-node lab, TLS, basic monitoring, test matrix | Complete | Re-validation in progress | [docs/01](docs/01-repo-versions-and-lab/README.md) |
| DEV-906 | Test data and verification | Synthetic dataset, versioning/object-lock/lifecycle/IAM fixtures, manifest generation and comparison tooling | Complete | Partial — open defects R7, R13 | [docs/02](docs/02-test-data-and-verification/README.md) |
| DEV-907 | MinIO feature validation | MinIO single-node feature validation | Complete | Not started | [docs/03](docs/03-minio-feature-validation/README.md) |
| DEV-908 | MinIO distributed mode | Distributed mode, resilience, healing, expansion | Complete | Not started | [docs/04](docs/04-minio-distributed-mode/README.md) |
| DEV-909 | MinIO replication | Bucket/batch/site replication and runbook | Complete | Not started | [docs/05](docs/05-minio-replication/README.md) |
| DEV-910 | MinIO performance baseline | `warp` profiles and storage-layer `fio` measurements | Complete | Not started — NFS cases blocked | [docs/06](docs/06-minio-performance-baseline/README.md) |
| DEV-911 | Silo functional validation | Silo functional validation in a comparable environment | Complete | Not started | [docs/07](docs/07-silo-functional-validation/README.md) |
| DEV-912 | Compatibility edge cases | Compatibility differences and O01–O08 | Complete | Not started | [docs/08](docs/08-compatibility-diff/README.md) |
| DEV-913 | Silo performance comparison | Identical benchmark methodology, side-by-side deltas | Complete | Not started — NFS cases blocked | [docs/09](docs/09-silo-performance-comparison/README.md) |
| DEV-914 | Security and licensing | CVE review, provenance, licence review, maintenance risk, exit strategy | Complete | Not started | [docs/10](docs/10-security-licence-review/README.md) |
| DEV-915 | Evaluation and recommendation | Capability matrix, executive report, risks, final recommendation | Complete | Not started | [docs/11](docs/11-evaluation-report/README.md) |

Main epic: [DEV-904](https://github.com/atiqa-ai/minio-vs-silo-evaluation/issues/1).

## Execution environment

Results are produced on a VMware guest with 4 vCPU, ~7.7 GiB RAM and a single
48 GB filesystem. The Profile B reference host requires at least 8 vCPU and 32
GiB, so this host is below the reference on both CPU and memory. **Every
performance result in this repository is therefore indicative, and none of it
establishes reference-host performance.**

Two separate problems are recorded here, and they should not be collapsed into
one:

- **The resource shortfall is a measurement limitation.** It bounds what any
  number produced here can support. Small differences between the two products may
  be noise, so the identical-methodology rule is enforced strictly and the
  comparison is useful as a *relative* indication rather than an absolute one.
- **The virtualisation is a governance question.** The requirements name a VMware
  guest as a prohibited environment (D-004), which under the earlier stop condition
  halted the Epic. D-019 records the decision to proceed anyway in an approved
  controlled reduced-resource environment. That is a recorded decision about
  whether to proceed; it is not evidence that the reference configuration was met,
  and nothing in this repository claims it was.

The gap is stated up front rather than discovered later, and is recorded per phase
in that phase's environment section: required specification, measured actual value,
container limits, the deviation and its reason, the effect on results, and the
residual risk to the conclusion.

## Where to start

| If you want to… | Read |
|---|---|
| Know what has been done and what has not | This file, then [DEVIATIONS.md](DEVIATIONS.md) |
| Review a phase before it is executed | [docs/03](docs/03-minio-feature-validation/README.md) — the first phase with no evidence yet |
| See the full phase-by-phase plan and gates | [DEV-904-EXECUTION-PLAN.md](DEV-904-EXECUTION-PLAN.md) |
| Review the lab and the evidence so far | [docs/01](docs/01-repo-versions-and-lab/README.md) |
| Review the test data and verification | [docs/02](docs/02-test-data-and-verification/README.md) |
| Rebuild the lab from scratch | [docs/01](docs/01-repo-versions-and-lab/README.md) §12 |
| See every departure from the requirements | [DEVIATIONS.md](DEVIATIONS.md) |
| Read the latest progress submission | [DEV-904-Daily-Report-2026-10-03.md](DEV-904-Daily-Report-2026-10-03.md) |
| Read the previous consolidated status | [DEV-904-Manager-Status-Report.md](DEV-904-Manager-Status-Report.md) |
| See the two open verification defects | [docs/02](docs/02-test-data-and-verification/README.md) — R7, R13 |

## Repository layout

```text
.
├── README.md                     # This file: status and navigation
├── DEVIATIONS.md                 # Every departure from the requirements, with reasons
├── DEV-904-EXECUTION-PLAN.md     # Phase plan, gates, dependencies, risk register
├── DEV-904-Manager-Status-Report.md    # Consolidated status for the project manager
├── DEV-904-Daily-Report-2026-10-03.md # Dated daily progress submission
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
│   ├── compose/               # minio, silo, replication-target, proxy,
│   │                          # workload, monitoring, storage
│   ├── images/                # minio, mc, fio, nfs — built locally, not pulled
│   ├── jobs/                  # benchmark job definitions (fio)
│   ├── data/                  # cluster data and generated dataset (not committed)
│   └── logs/                  # runtime logs (not committed)
└── tools/
    └── bin/                   # lab, gen-dataset, seed-dataset,
                               # capture-manifest, verify-manifest, and the
                               # check-* pre-commit hooks
```

Each `docs/NN-*` folder holds a `README.md` report, an `evidence/` directory of raw
command output, and a `screenshots/` directory. Evidence files are the primary
record; every PASS claim in a report is backed by one.

Seven Compose projects exist. All seven validate, and all seven are checked by the
mixed-cluster hook. `tools/bin/lab up <project>` is the supported entry point.

## Method

The comparison is only meaningful if the two products are measured identically, so
the lab enforces that structurally:

- **MinIO first, then Silo.** The same dataset, the same client binary, the same
  scripts, the same commands. Only the storage backend varies between runs. In
  particular the *same* client drives both products, so a difference cannot be
  attributed to the client.
- **No mixed clusters.** MinIO and Silo nodes are never placed in the same
  cluster. Enforced by a pre-commit hook that discovers its own inputs, and by
  `tools/bin/lab`, which refuses to start the replication target while Silo is
  running. The only permitted co-resident pair is the two MinIO deployments that
  DEV-909 genuinely requires, and that exception is confined in code rather than
  left in a comment.
- **Synthetic data only.** No real, company, or personal data is used anywhere.
- **Immutable image tags.** Every image is pinned by tag *and* registry digest,
  including `monitoring` and `warp`. `fio` and `nfs` are built locally from
  Dockerfiles in `lab/images/` rather than pulled.
- **Evidence before conclusions.** No result is written from memory or inference;
  raw command output is captured first, and stale or unsupported evidence is
  corrected rather than cited.
- **Failures stay failures.** A finding that cannot be reproduced is reported as
  such, including findings about the lab itself. A check that cannot run is
  recorded as *not available*, which is deliberately not the same as *failed*.

## Known limitations worth knowing before reviewing

- **The host is below the reference profile**, so performance results are
  *indicative* and cannot support capacity conclusions (D-004, D-019).
- **NFS is half-proven.** The NFS *server* side works — export, `rpc.nfsd`, and
  NFSv4 registration on port 2049 are all confirmed, after fixing a real defect in
  which `rpcbind` wedged NFSv4 registration. The NFS *client* side does not: v4
  mounts hang, with or without `nolock`, and v3 fails with `rpc.statd is not
  running` and then `Not supported`. NFS remains unproven end to end, so the
  NFS-backed storage comparisons in DEV-910 and DEV-913 are **not available**
  rather than failed. D-010 and D-018 still describe this tooling as unbuilt and
  need updating.
- **`fio` measures capability, not performance.** Back-to-back runs on the same
  volume differed by roughly 20%, and neither matched the one figure recorded from
  the original session. Until that variance is explained, fio output may only be
  used to show the tool runs.
- **Erasure coding doubles the disk footprint.** Four nodes with one drive each
  means a parity of two, so a 5.26 GiB dataset occupies roughly 11 GB on the
  volume. Capacity conclusions must be read in on-disk terms (D-016).
- **The dataset is below the Profile B floor.** Reduced dataset profiles
  (`reduced2g`, `reduced1g`) are used so the phases are executable at all; the
  Profile B 5–10 GB requirement is recorded as not met, with the measured value
  (D-020).
- **The configured `warp` profile does not fit the disk.** The original parameters
  require more space than the host has, so benchmark parameters are reduced and the
  reduction is recorded (D-021).
- **Two verification defects are open.** R7: multipart ETag verification compares
  a multipart ETag against a local MD5, so those objects cannot verify; the
  negative control that would prove it is still needed. R13: no real server-side
  capture has been generated and committed.
- **O01–O08 have an authoritative source.** Earlier revisions recorded O05 and O08
  as having no basis in the supplied requirements. The vendor publishes all eight
  compatibility conditions; they are captured as a documented vendor claim and then
  independently tested against both products (D-022).

## Repository security

This is a **public** repository and contains no credentials, internal hostnames,
domains, or addresses. `.env` files are excluded and only `.env.example`, holding
placeholders, is committed. `gitleaks` runs on every commit via a pre-commit hook
and has scanned the full history — 30 commits, no leaks.

Three further hooks run on commit: one rejects unpinned image tags, one rejects
MinIO and Silo sharing a cluster, and one rejects invented profile names and
affirmative compliance claims the host cannot support. The mixed-cluster hook
discovers its own input files, so it keeps working as the lab grows.

Note that the removal of fabricated specification citations was a manual audit, not
an automated check. No hook verifies that a cited rule exists, so a future edit
can reintroduce one; the sweep has to be re-run by hand.

`DEV-904-project-documentation-pack/` is agent instruction material, not project
content, and is deliberately excluded from version control.

## Licence and attribution

This repository contains the evaluation's own scripts, Compose definitions and
documentation. MinIO, Silo, and `warp` are third-party projects under their own
licences; their images are referenced by tag and digest and are not redistributed
here.