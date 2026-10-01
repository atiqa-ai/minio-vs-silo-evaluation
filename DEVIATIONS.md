# Deviations Register

Every departure from the SRD, the guardrails, or the prescribed test profile is
recorded here with its reason, its effect on the results, and whether it was
approved before or after the fact.

A deviation is not a failure. An *undisclosed* deviation is what makes an
evaluation worthless, because a reader cannot tell which conclusions the
deviation undermines.

Status values: `Approved` (agreed with the requester before acting) or
`Recorded` (necessary, discovered during work, and documented after the fact).

---

## D-001 — No public repository

| Field | Value |
|---|---|
| Affects | ST01 completion requirement "Public repository created" |
| Status | Approved |
| Decision | Keep the repository local at `/home/devops/Documents/minio-vs-silo-evaluation`. Do not push. |

**Reason.** The requester directed that the repository be set up locally and not
pushed.

**Effect.** The ST01 completion checklist item "Public repository created"
cannot be satisfied. All other ST01 requirements are met. Version control is
still in place — the repository is a normal Git repository with a committed
history, so it can be pushed to a public host at any time without changing the
content.

**Mitigation.** A remote has not been configured. The history is local-only.

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

## D-005 — Reduced dataset size

| Field | Value |
|---|---|
| Affects | ST02, ST04 |
| Status | Recorded |

**Reason.** Profile B specifies a 5–10 GB dataset. The host has roughly 18 GB
free and must hold the MinIO dataset, the Silo dataset, four images totalling
about 3.7 GB, and both clusters' volumes. A 10 GB dataset per product does not
fit.

**What was done instead.** A 2 GB dataset per product, plus a 256 MB small-object
subset. Both products receive byte-identical data generated by the same seed.

**Effect.** Multi-GB objects and very long object lists are not exercised. Write
and throughput behaviour at 2 GB is measured; behaviour at 10 GB is not.

---

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
be re-checked; the derived statements are collected in
`docs/00-srd/objectives-provisional.md`.

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

## D-010 — `fio` and NFS not available

| Field | Value |
|---|---|
| Affects | ST04, TC-ST04-11 |
| Status | Recorded |

**Reason.** `fio` is not installed, `nfs-kernel-server` is inactive, no NFS
kernel modules are loaded, and `sudo` requires interactive authentication that
cannot be provided in a non-interactive session.

**Effect.** Test cases that require raw device isolation or an NFS-backed mount
cannot be run as written. They are marked BLOCKED with this reason recorded,
rather than silently skipped or silently substituted. Substituting a different
storage technology would violate the Identical-Test Rule, so it is not done.

---

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