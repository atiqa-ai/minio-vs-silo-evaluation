# Deviations Register

Every departure from the SRD, the guardrails, or the prescribed test profile is
recorded here with its reason, its effect on the results, and whether it was
approved before or after the fact.

A deviation is not a failure. An *undisclosed* deviation is what makes an
evaluation worthless, because a reader cannot tell which conclusions the
deviation undermines.

Status values: `Approved` (agreed with the requester before acting) or
`Recorded` (necessary, discovered during work, and documented after the fact).

Register summary:

| ID | Subject | Status |
|---|---|---|
| D-001 | No public repository | Resolved 2026-10-01 |
| D-002 | MinIO CE image built from source | Recorded |
| D-003 | `mc` image built from release asset | Recorded |
| D-004 | Host below Profile B, benchmarks indicative | Recorded |
| D-005 | Dataset size, first pass under-sized | Resolved 2026-10-01 |
| D-006 | O01–O08 derived from the SRD, not supplied | Amended by D-022 — vendor source found |
| D-007 | Proxy ports moved off 8080 | Approved |
| D-008 | Load balancers gated on cluster state | Recorded |
| D-009 | Cluster data dirs are root-owned bind mounts | Recorded |
| D-010 | `fio` and NFS moved into containers | Recorded, **tooling not yet built** |
| D-011 | Go runtime differs between the servers | Recorded |
| D-012 | Execution order follows the SRD, not Jira keys | Approved |
| D-013 | `DEV-907` ran on the distributed profile | Recorded |
| D-014 | Prometheus and `warp` pinned by tag + digest | Recorded |
| D-015 | Cluster metrics endpoints require public auth | Recorded |
| D-016 | Erasure coding amplifies the dataset 2x on disk | Recorded |
| D-017 | Commit prefix uses the Jira key, not the subtask number | Recorded |
| D-018 | D-010 marked Resolved before the tooling existed | Recorded |
| D-019 | Execution in an Approved Controlled Reduced-Resource Environment | Approved |
| D-020 | Dataset below the Profile B floor, reduced profiles added | Approved |
| D-021 | Benchmark parameters reduced to fit available disk | Approved |
| D-022 | O01–O08 have an authoritative vendor source | Recorded |
| D-023 | `mcli` sourced from the pinned product image | Approved |
| D-024 | Documentation restructured to the phase model | Recorded |

---

## D-001 — No public repository *(RESOLVED 2026-10-01)*

| Field | Value |
|---|---|
| Affects | ST01 completion requirement "Public repository created" |
| Status | Resolved |
| Original decision | Keep the repository local at `/home/devops/Documents/minio-vs-silo-evaluation`. Do not push. |
| Reversed | 2026-10-01, on request: the repository is now published. |

**Original reason.** The requester directed that the repository be set up locally
and not pushed.

**Effect as originally recorded.** The ST01 completion checklist item "Public
repository created" could not be satisfied. All other ST01 requirements were
met. Version control was still in place — a normal Git repository with a
committed history, pushable to a public host without changing content.

**Resolution.** The requester subsequently directed strict compliance with the
supplied SRD, which requires a public GitHub repository (SRD section 12), commits
made directly to `main`, and Jira keys in issue titles. This deviation is
withdrawn and the requirement met:

* Repository: `https://github.com/atiqa-ai/minio-vs-silo-evaluation` (public).
* Branch: `main`.
* The one pre-existing commit was rewritten so its author email is the GitHub
  noreply address `230258577+atiqa-ai@users.noreply.github.com`, because SRD
  section 13 forbids committing email addresses and Git stores the author email
  in history.
* Commit messages use the Jira key first, then the ST id, satisfying both SRD
  section 12 and the Jira documentation rule.
* The Jira epic `DEV-904` and subtasks `DEV-905` … `DEV-915` exist as GitHub
  issues whose titles carry the Jira keys.

**Residual gap.** SRD section 12 also asks that the GitHub Project mirror the
Jira subtasks. Issue titles are done; the issues are not attached to a GitHub
Project board, because the SRD does not define one and guardrail 1 forbids
turning a general best practice into a project requirement. Recorded here rather
than silently omitted.

---

## D-002 — MinIO CE image built from source

| Field | Value |
|---|---|
| Affects | SRD 4.3 (pinned immutable image) |
| Status | Approved |

**Reason.** No pullable MinIO CE container image exists. Docker Hub
`minio/minio` returns HTTP 404, and `quay.io/minio/minio` returns HTTP 401.
MinIO's own download service no longer publishes container images, and the
historical binary host `dl.min.io` returns HTTP 410 Gone.

**What was done instead.** The MinIO server was built from the upstream source
tree at the last open-source release tag, using upstream's own build mechanism:

| Item | Value |
|---|---|
| Repository | `https://github.com/minio/minio` |
| Release tag | `RELEASE.2025-10-15T17-29-55Z` |
| Commit | `9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a` |
| Go toolchain | `go1.24.13 linux/amd64` |
| Build flags | `CGO_ENABLED=0 GOOS=linux GOARCH=amd64 -tags kqueue -trimpath` |
| Version injection | upstream `buildscripts/gen-ldflags.go`, `MINIO_RELEASE=RELEASE` |
| Binary SHA-256 | `15d7d777ed553352ff09a94ab4d5a0608aecb90448f1a5c8e7f2385eda8c32a9` |
| Binary version line | `minio version RELEASE.2025-10-15T17-29-55Z (commit-id=9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a)` |
| Base image | `registry.access.redhat.com/ubi9/ubi-micro@sha256:932aec77f5b86a5dba854a18b14a38725b296967e7dc9c7a1f4d7f0bf82e1ce5` |
| Local image | `minio-ce-local:RELEASE.2025-10-15T17-29-55Z` |
| Local image ID | `sha256:f71deba3825f2a57b4ab348b34aeec2fd1004c852f9d502f4d43dd17f7f4747a` |

**Effect.** The MinIO baseline is a faithful build of a specific pinned release
commit, but it is not bit-identical to any image the requester could have pulled.
The version string reported at runtime matches the tag exactly, and the commit
that produced the binary is recorded above.

**Base image choice.** `ubi9/ubi-micro` was selected because it is the same base
the Silo image is built on. Using the same base for both clusters removes base
OS and libc differences as a variable between the two products
(Identical-Test Rule, guardrails 6).

---

## D-003 — `mc` client image built from the official release asset

| Field | Value |
|---|---|
| Affects | ST01 tooling, ST06/ST07 client operations |
| Status | Recorded |

**Reason.** `minio/mc` was deleted from Docker Hub (HTTP 404) and `dl.min.io`
returns HTTP 410 Gone. The only remaining official distribution channel is the
GitHub release asset.

**What was done instead.** `mc-local:RELEASE.2025-08-13T08-35-41Z` was built from
the official release asset, checksum-verified before use.

| Item | Value |
|---|---|
| Release | `RELEASE.2025-08-13T08-35-41Z` |
| Commit | `7394ce0dd2a80935aded936b09fa12cbb3cb8096` |
| SHA-256 | `01f866e9c5f9b87c2b09116fa5d7c06695b106242d829a8bb32990c00312e891` |

**Effect.** The same `mc` binary is used against both products, so the client is
not a variable between the MinIO and Silo runs. Silo additionally ships its own
`mcli` inside its image; that difference is a finding for ST07, not a deviation.

---

## D-004 — Host is below Profile B, so all benchmarks are indicative

| Field | Value |
|---|---|
| Affects | ST04, ST05, ST08 |
| Status | Approved |

**Reason.** SRD 5 Profile B requires a host with at least 8 vCPU and 32 GB RAM.
The actual host has 4 vCPU and 7.7 GB RAM. The host is also itself a VMware
guest, which SRD names as a prohibited virtualisation environment.

**Actual host.**

| Resource | Profile B | Actual |
|---|---|---|
| vCPU | 8 | 4 |
| RAM | 32 GB | 7.7 GB |
| Disk free | — | ~18 GB of 48 GB |
| Virtualisation | bare metal | VMware guest |

**Effect.** **Every performance figure in this evaluation is indicative only.**
Absolute throughput and latency numbers must not be quoted as vendor
capabilities, and small differences between MinIO and Silo may be noise. The
comparison is still useful as a *relative* indication under identical
conditions, which is why the Identical-Test Rule is enforced strictly.

---

## D-005 — Dataset size: first pass under-sized, ST02 regenerating at 5 GB

| Field | Value |
|---|---|
| Affects | ST02, ST04 |
| Status | Recorded |
| Recorded | 2026-09-30 (revised) |

**Reason.** Profile B specifies a 5-10 GB dataset. The host has roughly 15 GB free
and must hold the source dataset, one cluster's data, four images totalling about
3.7 GB, and Prometheus time series. A 10 GB dataset per product does not fit, so
the ceiling of the profile range is out of reach.

**What was actually done.** The first generator iteration produced
**885.82 MiB / 928844494 bytes across 669 objects** — well short of the 5 GB floor
and *not* the 2 GB an earlier draft of this deviation claimed. That draft was
never reconciled against the generator's real output, so both the number in ST01
and this deviation were wrong. The shortfalls are real: neither a multi-GB single
object nor a long object list was exercised, so any write or throughput figure from
that dataset is not Profile B evidence.

**Correction now in force.** The generator is being re-run at the 5 GB Profile B
minimum, and `st02-verify` asserts the realised size against that floor rather than
trusting a hand-written claim. ST01's reference to a 2 GB dataset is corrected
here. If the host cannot hold 5 GB, the honest outcome is a recorded FAIL against
Profile B, not a silently smaller dataset described as compliant.

**Effect.** ST02 does not complete until the realised dataset is at or above 5 GB.
Benchmark results from the 885.82 MiB dataset are treated as invalid for Profile B
and are discarded rather than reported.

## D-006 — O01–O08 derived from the SRD, not supplied

| Field | Value |
|---|---|
| Affects | Every subtask that must cite an objective |
| Status | Approved |

**Reason.** The SRD refers to objectives O01–O08 but does not define them in the
supplied documents.

**What was done instead.** Each objective was derived from explicit SRD hints and
is labelled `provisional` wherever it is cited, per the approved decision.

**Effect.** Every objective reference in this repository points at a provisional
statement. If the authoritative O01–O08 text is provided later, the mapping must
be re-checked. The derived statements are reproduced below because the repository
does not carry the source requirement documents.

### Provisional objective mapping

| ID | Subject | Confidence | Where it would be covered |
|---|---|---|---|
| O01 | Cluster homogeneity, no product mixing | Implied | Enforced structurally; ST05, ST09 |
| O02 | Custom authorization policy behavior | Explicit | ST07 |
| O03a | Older authentication settings | Explicit | ST07 |
| O03b | Older notification settings | Explicit | ST07 |
| O04 | Programs relying on old bugs | Explicit | ST07 |
| O05 | Unknown | **No basis** | **Gap — not assessed** |
| O06 | Multi-pool behaviour | Explicit | Out of scope: single-pool topology |
| O07 | Replication and mixed-version | Explicit | Blocked by guardrails 11 |
| O08 | Unknown | **No basis** | **Gap — not assessed** |

O05 and O08 cannot be assessed at all: nothing in the supplied requirements states
what they are, so no evidence could exist for them. That is a gap in the
requirements, not a gap in the work.

---

## D-007 — Proxy ports moved off 8080

| Field | Value |
|---|---|
| Affects | SRD 4.4 port exposure |
| Status | Recorded |

**Reason.** The specification implies the load balancer on port 8080. On this host
`0.0.0.0:8080` is already held by a pre-existing `cadvisor` container that
belongs to an unrelated stack and must not be stopped, per the instruction to
avoid affecting the running Grafana, cadvisor, soul-of-lahore and
nginx-exporter containers.

**What was done instead.** Load balancers publish on `127.0.0.1:18080` (MinIO) and
`127.0.0.1:18081` (Silo). Console ports are `127.0.0.1:9001` (MinIO) and
`127.0.0.1:9011` (Silo).

**Effect.** None on results. The port number has no bearing on behaviour. The
move was in fact necessary: `lb-minio` could not have bound 8080 at all. It also
means the TC-ST01-08 wildcard-bind check cannot be confused by another stack's
ports.

---

## D-008 — Load balancers started only when their cluster is running

| Field | Value |
|---|---|
| Affects | ST01 lab operation, ST05 fault injection |
| Status | Recorded |

**Reason.** nginx resolves upstream hostnames while loading its configuration and
exits with `host not found in upstream` if any backend is absent. Starting
`lb-silo` before the Silo cluster existed therefore produced a crash loop rather
than a waiting proxy.

**What was done instead.** `tools/bin/lab up proxy` starts only the load balancer
whose backend cluster is actually running. Each proxy also serves a
`/healthz` endpoint that does not touch any upstream, so proxy health stays
meaningful while backend nodes are deliberately stopped during fault injection.

**Effect.** Load balancers are never crash-looping in captured evidence. An
operator must start a cluster before its proxy; the helper does this
automatically.

---

## D-009 — Cluster data directories are root-owned bind mounts

| Field | Value |
|---|---|
| Affects | Cleanup, ST12 |
| Status | Recorded |

**Reason.** Both servers run as root inside their container, so files written
under `lab/data/<product>/node-N` are owned by root on the host. The host user
cannot delete them with `rm`.

**Consequence.** Cleanup cannot be done by the invoking user. The documented
cleanup procedure runs a throwaway container as root over the bind mount. This
matters because guardrails 20 requires reproducible teardown: an operator who
follows a naive `rm -rf lab/data` will get permission errors and may conclude the
lab is still in use.

---

## D-010 — `fio` and NFS moved into containers (no longer blocked)

| Field | Value |
|---|---|
| Affects | ST04, TC-ST04-11 |
| Status | Recorded — **tooling not yet built, see D-018** |
| Recorded | 2026-09-30 |

**Reason, as originally recorded.** `fio` was not installed, `nfs-kernel-server`
was inactive, no NFS kernel modules were loaded, and `sudo` required interactive
authentication unavailable in a non-interactive session. Installing packages on
the host was also undesirable, since the host is shared with other projects and
mutating it would make the evaluation harder to reproduce.

**What was intended.** This was an environmental blocker, not a requirement
problem. The intent was to run both tools in purpose-built containers with the
same isolation as the rest of the lab: `fio` in its own image against the storage
under test, and NFS served by a container exporting the dataset directory. Nothing
would be installed on the host, and no existing container on this host modified.

**Effect, as of 2026-10-01.** The containerised tooling **does not exist yet**:
there is no `fio` or NFS Compose service, no wrapper script, and no evidence file
for either, in this repository as it stands. The decision to containerise is
recorded and remains sound, but the claim that these cases are no longer blocked
is withdrawn until the containers exist. See D-018. TC-ST04-11 and the NFS cases
are therefore **not yet executable**, which is a different thing from failed.

## D-011 — Go runtime differs between the two servers

| Field | Value |
|---|---|
| Affects | ST08 performance comparison |
| Status | Recorded |

**Reason.** The two servers are not built with the same Go toolchain, and this
affects scheduler behaviour in a way that is visible under CPU limits.

| Product | Release | Go runtime |
|---|---|---|
| MinIO CE | `RELEASE.2025-10-15T17-29-55Z` | `go1.24.13` |
| Silo | `RELEASE.2026-09-16T00-00-00Z` | `go1.27.1` |

Silo logs this at startup:

```
WARN: Detected GOMAXPROCS(2) < NumCPU(4); provide all processors to Silo for optimal performance
```

Go 1.25 and later derive `GOMAXPROCS` from the cgroup CPU quota. Under the
identical `cpus: 0.80` limit applied to both clusters, Silo resolves this to
`GOMAXPROCS(2)`, whereas the Go 1.24-built MinIO does not perform that
adjustment.

**Effect.** This is a genuine property of the products being compared, not a
laboratory artefact, and it cannot be removed without changing what is being
tested. It is recorded because it is a plausible contributor to any throughput
difference observed in ST08, and attributing such a difference purely to "Silo
is faster or slower" would be unsound. Any ST08 conclusion must state which Go
runtime produced it.

---

## D-012 — Execution order follows the SRD, not the Jira key order

| Field | Value |
|---|---|
| Affects | ST04, ST05 |
| Status | Approved |

**Reason.** The supplied Jira reference numbers the subtasks in a different
order from the requirements' `ST01`–`ST10`. That document is not committed here.
Two differences matter:

| Subject | Jira | SRD |
|---|---|---|
| MinIO replication | separate subtask `DEV-909` | folded into ST05 |
| MinIO performance baseline | `DEV-910`, listed *after* `DEV-909` | `ST04`, *before* `ST05` |

The Jira execution sequence is `DEV-905 → … → DEV-908 → DEV-909 → DEV-910 → …`,
which runs replication before performance. The SRD requires
`ST04 (performance) → ST05 (distributed mode, which includes replication)`.

**What was done instead.** The SRD execution order is authoritative, so ST04 is
executed before ST05. Guardrail 29 states that the approved SRD takes priority
over model suggestions and general practice, and guardrail 1 forbids changing
the project's testing methodology without a documented requirement. The Jira
document is used as a **tracking map**: `DEV-905`–`DEV-915` identify work, and
every commit, issue and subtask README cites its Jira key, but the ST sequence
decides what runs when.

**Effect.** The repository's folder structure and execution order remain exactly
as SRD section 10 defines them. Replication (`DEV-909`) is covered inside
`docs/04-minio-distributed-mode/` beside `DEV-908`, because adding a folder for it
would add structure the SRD does not define (guardrail 17). No test, evidence
item or result changes; only the order in which the same work is scheduled
differs from the Jira ticket numbering.

---

## D-013 — `DEV-907` executed on the distributed profile, not single node

| Field | Value |
|---|---|
| Affects | ST03 |
| Status | Approved |

**Reason.** The Jira reference titles `DEV-907` "MinIO feature validation (single
node)". The SRD's ST03 says only "MinIO feature validation" and specifies no
node count, while SRD section 5 makes a 4-node cluster plus a load-balancer
container the reference Profile B topology. The SRD therefore both fixes the
topology and stays silent on node count.

**What was done instead.** ST03 runs against the Profile B 4 nodes x 1 drive
cluster. Guardrail 1 forbids turning a Jira title into a project requirement the
SRD does not state, and SRD section 5 is the higher authority on topology.

**Effect.** Feature results (versioning, object lock, lifecycle, core S3
operations) are validated on the distributed topology the SRD mandates. They are
*not* separately validated against a single-node MinIO deployment, so ST03's
evidence does not demonstrate single-node behaviour. This is restated in
`docs/03-minio-feature-validation/README.md` so it cannot be read as coverage that
was never performed.

## D-014 — Prometheus and `warp` pinned by semver tag + registry digest

|---|---|
| Affects | ST01, ST04, ST05, ST07 |
| Status | Approved |
| Recorded | 2026-09-30 |

**Reason.** The project pins every image by immutable release tag so a result can
be reproduced. MinIO, Silo, and `mc` all publish `RELEASE.<timestamp>` tags, so
that convention is satisfied for them. `prom/prometheus` and `minio/warp` publish
**no** `RELEASE.*` tags at all: the registry only carries moving tags such as
`latest`, `v3.15.0`, and `v3.13.4`. Neither is archived, so `latest` would silently
break reproducibility between two runs of this evaluation.

**What was done instead.** Both are pinned by *both* an immutable semantic-version
tag *and* the resolved registry digest, which is the only form that cannot drift:

| Image | Pinned reference |
|---|---|
| Prometheus | `prom/prometheus:v3.15.0@sha256:efd719c99d83b060d9daefdcf00360461adf279f45ef5391f8d111892118753e` |
| `warp` | `minio/warp:v1.3.1@sha256:72ae1b02216b51bd102b73a6923b597c092a5acc7a655c936c2f31bee897a7c5` |

**Effect.** Reproducibility is preserved — equal to the `RELEASE.*` guarantee, and
in fact stricter, because the digest cannot be re-pointed by a publisher. The only
deviation from the project's convention is the *naming* of the version, which is
recorded here rather than presented as compliance. The digests are resolved from
the local daemon and are recorded in `lab/compose/.env.example`, which is tracked;
`.env` itself stays untracked.

## D-015 — Cluster metrics endpoints require public Prometheus auth

|---|---|
| Affects | ST01, ST07 |
| Status | Approved |
| Recorded | 2026-09-30 |

**Reason.** SRD 4.4 requires a `monitoring` Compose project, and SRD 4.4 also
forbids any project other than the consoles and the proxy from publishing ports.
That combination leaves the scraper with no host-reachable path, so it must scrape
over `migration-net`. Doing so initially failed: every node answered
`403 Forbidden` on `/minio/v2/metrics/cluster`, and Prometheus recorded all four
MinIO targets as `down`. The endpoint is authenticated by default.

**What was done instead.** `MINIO_PROMETHEUS_AUTH_TYPE=public` was set on all four
nodes of **both** clusters — deliberately identical, so the metric surface stays
comparable between products (guardrail 6) and so neither product gains an
advantage from a lab-side difference. The raw `403` state and the post-fix `up`
state are both recorded in `docs/01-repo-versions-and-lab/evidence/TC-ST01-06-minio.txt`.

**Effect.** Metrics collection works and no monitoring port is published:
`HostConfig.PortBindings` for `lab-prometheus` is `{}`, verified in
`TC-ST01-07-minio.txt` and `TC-ST01-08-minio.txt`. This is a lab-side observation,
not a product finding: it must not be reported as "MinIO and Silo differ on
metrics auth", because both were changed identically and no comparison was made.

---

## D-016 — Erasure coding amplifies the dataset 2x on disk

| Field | Value |
|---|---|
| Status | Recorded |
| Recorded | 2026-10-01 |
| Affects | SRD 6 (storage requirements), ST02, ST08 |

**Reason.** SRD 5 (Profile B) sizes the dataset at 5–10 GB and assumes that figure
is what the lab must hold for two products. That is the logical object size, not
the on-disk size. Each cluster is four nodes with one drive each, so MinIO selects
a default parity of two and distributes every object across the set as two data
plus two parity shards.

**Measured.** `mc du` reports `5.3GiB` and `2409 objects` for the seeded bucket,
while `du` on `lab/data/minio` reports `11G` — a ratio of `2.01x` on the one
bucket measured. The same amplification applies to the Silo turn. It was not
predicted in advance and no authoritative confirmation of the parity setting has
been recorded yet; the ratio is a measurement, and the parity inference from it is
not yet evidence.

**Effect.** The capacity that actually has to exist per product is roughly double
the SRD figure: a 5.26 GiB dataset occupies about 11 GB in MinIO and would occupy
a comparable amount in Silo, plus the local copy of the same data. On the 48 GB
host this is what exhausts the volume, and it is why only one heavy stack can be
resident at a time. Any capacity conclusion in ST08 must be stated in on-disk
terms, with the amplification stated alongside it, or it will understate Silo's
and MinIO's real footprint by half.

---

## D-017 — Commit prefix uses the Jira key, not the subtask number

| Field | Value |
|---|---|
| Status | Recorded |
| Recorded | 2026-10-01 |
| Affects | SRD 12 (public repository requirements) |

**Reason.** SRD 12 states that commit messages "should start with the subtask
number", giving `ST05: add site replication steps` as the example. Every commit in
this repository instead begins with the Jira key, for example
`DEV-905: ST01 add the required monitoring project and correct the dataset claim`.

**Reason for the departure.** Jira key-first was chosen so that every commit is
greppable from the issue tracker, and SRD 12 separately requires the Jira key in
issue titles. The subtask number is retained as the second token, so both remain
present.

**Effect.** Traceability is preserved in substance; the literal prefix format does
not match the SRD example. Nothing in the evaluation depends on it. Recorded rather
than corrected, because the current form is the more useful one and changing six
commits to satisfy a formatting example would rewrite published history for no
gain. If the requester prefers strict conformance, the history can be rewritten
before any external reader depends on it.

---

## D-018 — D-010 marked Resolved before the tooling existed

| Field | Value |
|---|---|
| Status | Recorded |
| Recorded | 2026-10-01 |
| Affects | ST02, D-010 |

**Reason.** D-010 records that `fio` and NFS were moved from the host into
containers so that both products could be measured identically. Its status is
`Resolved`. No such containerised tooling is present in the repository: there is
no Compose service, no script, and no evidence file for either `fio` or NFS, and
no NFS server is defined in either cluster.

**Effect.** D-010 as written claims a capability the lab does not have. Any reader
taking ST02's storage-testing claims at face value would conclude the
containerised path was built and exercised. The claim is withdrawn here until the
tooling exists; the underlying decision to containerise is still sound and the
`fio` and NFS test cases in ST02 remain unimplemented rather than failed.

---

## D-019 — Execution proceeds in an Approved Controlled Reduced-Resource Environment

| Field | Value |
|---|---|
| Affects | Every phase; supersedes the *basis* of D-004 without contradicting it |
| Status | Approved |
| Recorded | 2026-10-03 |
| Supersedes | The treatment of the virtualisation prohibition in D-004; the numeric figures in D-004 still stand |

**Problem.** D-004 records two facts: the host is below the Profile B reference, and
the host is a VMware guest, which the requirements name as a prohibited
virtualisation environment. Under the earlier stop condition, the second fact halted
the Epic.

**Decision.** Execution is authorised in an **Approved Controlled Reduced-Resource
Execution Environment**. The VMware guest and the reduced resources are approved
conditions of execution. Profile A and Profile B requirements are unchanged. This is
**not** a new profile, and no artefact may state that Profile A or Profile B was
completed.

**Action.** Every phase records, in its environment section: required specification,
measured actual value, container limits, the deviation and its reason, the effect on
results, and residual risk to the conclusion. Two consequences are stated up front
rather than discovered later:

1. Performance figures cannot support capacity or production-sizing conclusions.
2. The dataset is below the Profile B floor (see D-020).

**Effect.** The Epic proceeds instead of halting, and the environmental gap becomes
auditable per phase instead of being a single unreconciled footnote. The obligation
to be explicit about the gap is *increased*, not relaxed, because a controlled
environment is only defensible if it is documented precisely.

**Measured against D-004.** The vCPU and RAM shortfall in D-004 is unchanged and is
re-measured per phase. The virtualisation prohibition is the element superseded here.

---

## D-020 — Dataset below the Profile B floor, reduced profiles added

| Field | Value |
|---|---|
| Affects | DEV-906, DEV-910, DEV-911, DEV-913 |
| Status | Approved |
| Recorded | 2026-10-03 |

**Problem.** The Profile B dataset floor is 5–10 GB, enforced in `gen-dataset` by
`PROFILE_B_MIN_BYTES = 5 GiB` and by `--min-bytes`. On a single 48 GB filesystem
with parity-2 erasure amplification, a 5.26 GiB dataset occupies roughly 11 GB per
cluster, and DEV-909 requires two clusters resident at once. The Profile B dataset
requirement could not coexist with the rest of the work.

**Decision.** Add reduced dataset profiles as **additional generator keys**. The
existing `full`, `profileb` and `smoke` profiles are never resized in place, because
doing so would invalidate every digest already recorded against them.

**Action and measured sizes.** Verified by recomputing the generator's plan function
rather than by assertion:

| Profile | Objects | Realised | Parity-2 cluster | Used by |
|---|---|---|---|---|
| `profileb` (unchanged) | 2,409 | 5.264 GiB | 10.8 GiB | reference |
| `reduced2g` | 2,383 | 2.014 GiB | 4.027 GiB | DEV-906/907/908/910/911/912/913 |
| `reduced1g` | 2,375 | 1.014 GiB | 2.027 GiB | DEV-909, two concurrent deployments |

Non-large categories are unchanged, so key shapes, retention modes, tags, LIST depth
and the 128 MiB large-object size are preserved. `--min-bytes` is set to each
profile's own floor, so the tool records `meets_profile_b_floor: false` against the
Profile B floor itself. The required-versus-actual record is therefore produced by the
tool, not asserted in prose.

**Effect.** The Profile B dataset requirement is **not met** and is recorded as not
met wherever it applies. The declared cost: large-object count falls from 40 to 14 or
6, which reduces multi-object erasure coverage and large-object sample size. Any
conclusion about large-object throughput rests on fewer samples than Profile B
intended, and that limitation travels with the number.

**Verification.** Recomputing `profileb` reproduced the previously recorded result of
2,409 objects and 5,651,848,823 bytes exactly, confirming the reduced-profile
arithmetic is derived from the same generator logic as the original evidence.

---

## D-021 — Benchmark parameters reduced to fit available disk

| Field | Value |
|---|---|
| Affects | DEV-910, DEV-913 |
| Status | Approved |
| Recorded | 2026-10-03 |

**Problem.** The `warp` profile in `lab/compose/.env.example` specifies 200 objects of
64 MiB, which is 12.5 GB of logical data and roughly 25 GB once parity-2 erasure
amplification is applied. The host had 608 MB free. The configured benchmark could
not run at all — this was a hard blocker on the performance phases, not merely an
accuracy caveat.

**Decision.** Reduce the benchmark parameters so the phases are executable, and record
the reduction rather than presenting reduced numbers as if they were the configured
ones.

**Action.** Parameters are set per phase against measured free space, and each
performance artefact records the configured value, the used value, the reason, and
the effect on comparability. Repeated runs and variance are retained, because the
reduction affects scale, not repeatability.

**Effect.** Throughput figures describe a smaller working set than Profile B
intended. Small differences between MinIO and Silo are more likely to be noise at
this scale. Together with D-019 this means performance output is *indicative under a
controlled environment* and is not evidence of production capacity.

---

## D-022 — O01–O08 have an authoritative vendor source; recorded "no basis" withdrawn

| Field | Value |
|---|---|
| Affects | DEV-912 |
| Status | Recorded |
| Recorded | 2026-10-03 |
| Amends | D-006 |

**Problem.** D-006 records that the O01–O08 objectives were derived from the SRD
rather than supplied, and that O05 and O08 had no basis in the supplied requirements,
so no evidence could exist for them. The README repeated this. On checking, the
reason was incomplete: the SRD genuinely does not define all eight, but the vendor
publishes all eight compatibility conditions, including the two that appeared to
have no basis.

**Decision.** The vendor's published compatibility page is the authoritative source
for the **wording** of O01–O08. It is a **vendor claim**, not a verified behaviour.
The wording is captured with URL and retrieval date; the behaviour is then
independently tested against both products, and every conclusion comes from our test
results rather than from the vendor's description.

**Action.** Capture all eight conditions in DEV-912 with retrieval date and evidence
reference. For each condition record an applies / does-not-apply decision backed by a
test against both products.

**Effect.** O05 and O08 move from "not assessable" to assessable. The claim that they
had no basis is withdrawn. The residual limitation is stated plainly: the requirement
text originates with the vendor being evaluated, so it is labelled a documented claim
wherever it is cited, and never used as proof that the products behave as described.

---

## D-023 — `mcli` sourced from the pinned product image rather than downloaded

| Field | Value |
|---|---|
| Affects | DEV-905, DEV-911, DEV-912 |
| Status | Approved |
| Recorded | 2026-10-03 |

**Problem.** `mcli` is absent from the host, and Silo's documentation directs users to
run `mcli` against Silo. Downloading it separately would introduce an unpinned
external binary into a project whose rules require pinned, reproducible tooling.

**Decision.** Extract `mcli` from the same pinned Silo image the product is tested
from, and record its version and checksum.

**Basis.** The image layer history shows `COPY /go/bin/mcli /usr/bin/mcli`,
`chmod +x /usr/bin/silo /usr/bin/mcli`, `ln -sf mcli /usr/bin/mc`, and `curl` baked
in. The image is the classic variant, not `-distroless`.

**Two consequences.**

1. The distroless question is settled by evidence rather than preference: the
   distroless variant ships the binary alone, with no shell, `mc` or `curl`, so the
   shell-based entrypoint and in-container client workflow this lab uses require the
   classic variant.
2. The image symlinks its `mcli` as `mc`. Using Silo's `mcli` against Silo while
   using MinIO's `mc` against MinIO would mean the two products were driven by
   different clients, which violates the Identical-Test Rule. **One client drives both
   products**: MinIO's `mc` is used against both, and `mcli` is used only where it is
   the only option, with both versions recorded in the fairness record. Any behaviour
   that differs under `mc` is a DEV-912 compatibility finding, not a tooling artefact.

**Effect.** The client-fairness requirement is satisfied structurally rather than by
assertion, and no unpinned binary enters the project.

---

## D-024 — Documentation restructured to the phase model; governance documents at root

| Field | Value |
|---|---|
| Affects | Whole repository |
| Status | Recorded |
| Recorded | 2026-10-03 |
| Reverses | Commit `20a46b9`, which removed the governance documents |

**Problem.** The repository carried an `ST01`–`ST10` documentation structure while the
project requirements define a `DEV-905`–`DEV-915` phase model with 11 phase
directories. Documentation removed by `20a46b9` was recoverable only from Git history.
Repository status tables also conflicted with measured reality.

**Decision.** Migrate the documentation with `git mv` so history is preserved, restore
the governance documents to the repository root, and reconcile the status tables to
measured state rather than to the old tracker.

**Action and mapping.** Eleven phase directories now match the phase plan. Phase
directory names were taken from the project requirements, not invented:

| Old | New |
|---|---|
| `01-repository-and-lab` | `01-repo-versions-and-lab` |
| `02-test-data-and-verification` | unchanged |
| `03-minio-feature-validation` | unchanged |
| `04-minio-performance-baseline` | `06-minio-performance-baseline` |
| `05-minio-distributed-mode` | `04-minio-distributed-mode` |
| *new* | `05-minio-replication` |
| `06-silo-functional-validation` | `07-silo-functional-validation` |
| `07-s3-client-compatibility` | `08-compatibility-diff` |
| `08-silo-benchmark` | `09-silo-performance-comparison` |
| `09-security-licensing-maintenance` | `10-security-licence-review` |
| `10-capability-matrix-evaluation` | `11-evaluation-report` |

References were rewritten in code, scripts and prose. **Captured evidence files were
not edited**: `docs/01-repo-versions-and-lab/evidence/secret-scanning.txt` still
records the path as it stood at capture time, which is correct, because editing
evidence after capture would falsify it.

**Effect.** Documentation matches the phase model, links resolve, and the directory
order reflects the execution order rather than the numeric issue-key order. Prior
evidence remains intact and traceable.
