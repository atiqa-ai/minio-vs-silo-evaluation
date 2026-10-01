# ST01 — Repository and Lab

## 1. Goal

Set up the repository, pin every version, and build a working local Docker
Compose lab in which a MinIO CE cluster and a Silo cluster can be started,
verified and compared under identical conditions.

This subtask does not measure performance or judge compatibility. It establishes
that the lab is trustworthy, so that later subtasks can rely on it.

## 2. Environment

Host, captured in `evidence/TC-ST01-01-minio.txt`:

| Item | Value |
|---|---|
| OS | Ubuntu, linux/amd64 |
| Kernel-reported CPUs | 4 |
| Memory | 8,273,563,648 bytes (7.7 GiB) |
| Docker Engine | 29.1.3, API 1.52 |
| Docker Compose | v2.40.3+ds1-0ubuntu1 |
| Storage driver | overlayfs |
| Cgroup driver / version | systemd / v2 |
| containerd / runc | 2.2.2 / 1.4.0 |
| Docker root dir | `/var/lib/docker` |
| Root filesystem | `/dev/sda2`, 48 G total, 18 G free at capture |
| Virtualisation | VMware guest — a prohibited environment per SRD |

Because the host is below Profile B on CPU and memory, and is itself
virtualised, **every measurement in this evaluation is indicative only**. See
`DEVIATIONS.md` D-004.

Images used, all pinned and digested:

| Image | Pin | Image ID / digest |
|---|---|---|
| MinIO CE | `minio-ce-local:RELEASE.2025-10-15T17-29-55Z` | `sha256:f71deba3…f4747a` |
| Silo | `pgsty/silo:RELEASE.2026-09-16T00-00-00Z` | `sha256:635197cb…e51a46` |
| `mc` | `mc-local:RELEASE.2025-08-13T08-35-41Z` | `sha256:80d58ab8…b382d2` |
| `warp` | `minio/warp:v1.3.1` | `sha256:72ae1b02…97a7c5` |
| proxy | `nginx:1.27-alpine` | `sha256:65645c7b…f2a10` |

The MinIO and `mc` images are built locally from checksum-verified upstream
artefacts because no pullable images exist for them (`DEVIATIONS.md` D-002,
D-003).

## 3. Prerequisites

- Docker Engine with Compose v2 — verified, not assumed.
- `docker network create migration-net` available.
- No root required. Every helper runs as the invoking user.
- Approximately 5 GB of free disk for images and one cluster's data.

No `sudo` is used anywhere in this repository, because sudo requires interactive
authentication that cannot be provided non-interactively. Where a task would
normally need it, the task is reimplemented user-locally or marked BLOCKED with
the reason recorded.

## 4. Step-by-step procedure

```bash
cd /home/devops/Documents/minio-vs-silo-evaluation

# 1. Shared network (created once; idempotent)
./tools/bin/lab network

# 2. MinIO baseline cluster: 4 nodes x 1 drive, plus its load balancer
./tools/bin/lab up minio
./tools/bin/lab up proxy

# 3. Capture ST01 evidence for the MinIO baseline
./tools/bin/st01-verify minio

# 4. Tear the baseline down before starting Silo: guardrails 15 forbids
#    running both heavy stacks at once
./tools/bin/lab down minio
./tools/bin/lab down proxy

# 5. Silo cluster, identical topology and limits
./tools/bin/lab up silo
./tools/bin/lab up proxy

# 6. Capture ST01 evidence for the Silo pass
./tools/bin/st01-verify silo
```

The MinIO baseline is left running after ST01, because the required execution
order is MinIO first for every test from ST02 onwards.

Secret scanning is installed separately, once:

```bash
./tools/bin/install-hooks      # writes .git/hooks/pre-commit
```

## 5. Expected result

- All four Compose projects validate with `docker compose config -q`.
- Both clusters form a single erasure pool of one set with four drives.
- Every node reports `Network: 4/4 OK`, `Drives: 1/1 OK`, `Pool: 1`.
- `migration-net` is the only network any lab container is attached to.
- The only published ports are the two node consoles and the two load
  balancers, each bound to `127.0.0.1`.
- The S3 API port 9000 is not published on any cluster node.
- A commit containing credentials is rejected.

## 6. Actual result

All eight test cases passed in **both** the MinIO and the Silo pass.

| Evidence | Covers |
|---|---|
| `evidence/TC-ST01-01-{minio,silo}.txt` | Docker environment, storage, disk |
| `evidence/TC-ST01-02-{minio,silo}.txt` | Compose v2, all four projects validate |
| `evidence/TC-ST01-03-minio.txt` | MinIO tag, image ID, source provenance, runtime version |
| `evidence/TC-ST01-04-silo.txt` | Silo tag, image digest, server and `mcli` versions |
| `evidence/TC-ST01-05-{minio,silo}.txt` | `migration-net` exists; every lab container on exactly one network |
| `evidence/TC-ST01-06-{minio,silo}.txt` | All nodes healthy, all reachable, cluster topology, DNS |
| `evidence/TC-ST01-07-{minio,silo}.txt` | Published ports limited to console and proxy |
| `evidence/TC-ST01-08-{minio,silo}.txt` | Every published port bound to loopback |
| `evidence/minio-build-provenance.txt` | Full MinIO source-to-image provenance chain |
| `evidence/secret-scanning.txt` | Secret scan setup and behaviour |

Both products formed the identical topology, confirmed from server logs:

```
MinIO: Formatting 1st pool, 1 set(s), 4 drives per set.
Silo:  Formatting 1st pool, 1 set(s), 4 drives per set.
```

Every node of both clusters reported `Network: 4/4 OK`, `Drives: 1/1 OK`,
`Pool: 1`.

## 7. PASS/FAIL

**ST01: PASS**, with one requirement not met by decision.

| Completion requirement | Status | Evidence |
|---|---|---|
| Public repository created | **NOT MET — see D-001** | Requester directed a local-only repository; Git history exists but has no remote |
| Docker environment ready | PASS | `TC-ST01-01-minio.txt` |
| Docker Compose v2 ready | PASS | `TC-ST01-02-minio.txt` |
| MinIO version pinned | PASS | `TC-ST01-03-minio.txt` |
| Silo version pinned | PASS | `TC-ST01-04-silo.txt` |
| Image digests recorded | PASS | both files above |
| `migration-net` configured | PASS | `TC-ST01-05-minio.txt` |
| Required Compose projects configured | PASS | `TC-ST01-02` and `TC-ST01-06` |
| Required port exposure configured | PASS | `TC-ST01-07`, `TC-ST01-08` |
| Secret scanning / pre-commit scanning active | PASS | `evidence/secret-scanning.txt` |

Repository evidence — Compose files, digests, `docker compose ps`, environment
information and command output — is present under `lab/compose/` and `evidence/`.

One requirement is unmet, and it is unmet by explicit decision rather than by
omission. D-001 records it.

## 8. Results table

### Lab topology

| Component | MinIO | Silo | Identical? |
|---|---|---|---|
| Nodes | 4 | 4 | yes |
| Drives per node | 1 | 1 | yes |
| Erasure pools / sets | 1 / 1 | 1 / 1 | yes |
| CPU limit per node | 0.80 | 0.80 | yes |
| Memory limit per node | 900 MB | 900 MB | yes |
| Data location | `lab/data/minio/node-N` bind mount | `lab/data/silo/node-N` bind mount | same type |
| Base image | `ubi9/ubi-micro` | `ubi9/ubi-micro` | yes |
| Network | `migration-net` | `migration-net` | yes |
| Go runtime | `go1.24.13` | `go1.27.1` | **no — D-011** |

### Published ports

| Service | Host binding | Published? |
|---|---|---|
| MinIO node 1 console | `127.0.0.1:9001` | yes — console |
| MinIO nodes 2–4 | none | no |
| MinIO S3 API (all nodes) | none | **no** |
| `lb-minio` | `127.0.0.1:18080` | yes — proxy |
| Silo node 1 console | `127.0.0.1:9011` | yes — console |
| Silo nodes 2–4 | none | no |
| Silo S3 API (all nodes) | none | **no** |
| `lb-silo` | `127.0.0.1:18081` | yes — proxy |
| `mc-client`, `silo-client` | none | no |

Pre-existing containers outside this project (`grafana` on `0.0.0.0:3001`,
`cadvisor` on `0.0.0.0:8080`, `soul-of-lahore`, `nginx-exporter`) were left
running and untouched. TC-ST01-08 records them explicitly as *not* this
project's ports, so their wildcard bindings cannot be mistaken for a guardrail
failure here.

## 9. Findings and problems

Problems found and fixed during this subtask, in the order they were found:

**9.1 — `lab/compose/.env` would have been committed with live credentials.**
The original `.gitignore` was written before the Compose lab existed and did not
exclude `.env`. Staging the repository put the populated credential file into
the Git index. Fixed by rewriting `.gitignore`; verified that
`git check-ignore lab/compose/.env` matches and that staging produces zero `.env`
files while `.env.example` (placeholders only) remains tracked. This is the
single most consequential defect found in ST01.

**9.2 — Load balancer ports collided with another stack.** `MINIO_PROXY_PORT=8080`
was unusable: a pre-existing `cadvisor` container already holds
`0.0.0.0:8080`, and it must not be stopped. Moved to `18080`/`18081`
(`DEVIATIONS.md` D-007).

**9.3 — TC-ST01-08 initially reported a false failure.** The first version of the
wildcard-bind check scanned all host listening sockets, so it matched cadvisor's
`0.0.0.0:8080` and reported FAIL for something this project does not own. The
check was rewritten to assert only the lab's own ports. The original false
failure is recorded here rather than deleted, per guardrails 13.

**9.4 — `lb-silo` crash-looped when started without its cluster.** nginx resolves
upstream hostnames at config load and exits with `host not found in upstream`.
Starting the Silo proxy before the Silo cluster produced a permanent restart
loop. Fixed by making `lab up proxy` start only the balancer whose cluster is up
(D-008), and by adding a `/healthz` endpoint that does not touch an upstream, so
proxy health survives deliberate backend outages during ST05 fault injection.

**9.5 — `nginx -t` cannot be verified off-network.** Running the syntax check in a
throwaway container outside `migration-net` fails with the same upstream
resolution error, because the container cannot resolve the node names. The check
is only meaningful on `migration-net`, or with upstreams substituted. Recorded so
a future reader does not misread that failure as a config syntax error.

**9.6 — Evidence contradicted live state once.** An early TC-ST01-07 capture
showed `lb-silo` publishing nothing while the container was in fact publishing on
18081, because Docker populates port metadata asynchronously after a container
reports started. A settle delay was added so evidence is captured from a settled
system. Evidence that disagrees with live state is worse than no evidence, so
this was re-captured rather than annotated.

**9.7 — Custom gitleaks rules initially used unsupported regex.** gitleaks uses
RE2, which has no lookahead; `(?!` caused a panic. Rewritten using character
classes that structurally exclude placeholders, so `<SECRET_KEY>` and `${VAR}`
cannot match while a real credential can.

Observations recorded for later subtasks:

- Silo accepts `minio server ...` and bare `server ...` as aliases for its server
  binary. Noted for ST07; the lab uses the explicit `silo` form so it does not
  depend on alias behaviour.
- `silo --commit` and `mcli --commit` are **not** valid flags, although MinIO
  accepts `--commit`. The commit is still visible in `--version` output. A real,
  minor CLI surface difference for ST07.
- Silo logs `WARN: Detected GOMAXPROCS(2) < NumCPU(4)` under the 0.80 CPU limit.
  Go 1.25+ derives `GOMAXPROCS` from the cgroup quota; the Go 1.24-built MinIO
  does not. Recorded as D-011 because it is a plausible contributor to any ST08
  throughput difference and must not be silently attributed to either product.

## 10. Conclusion

The lab is trustworthy enough to build the rest of the evaluation on.

Both products run the specified 4-node × 1-drive topology in a single erasure
pool from the same base image, under identical CPU, memory and volume limits, on
a single shared network, with only consoles and load balancers published and all
of them on loopback. Client tooling runs as containers on the same network, so
the S3 API is never exposed to the host or the internet. Versions are pinned by
immutable tag and digest, and the MinIO baseline carries a complete
source-to-image provenance chain. Credentials are synthetic and excluded from
version control by both `.gitignore` and an active pre-commit secret scan.

The one requirement not met is the public repository, unmet by explicit decision
(D-001), not by oversight.

Three limits are inherited from the host and must be restated in the final
recommendation: benchmarks are indicative only (D-004), the dataset is 2 GB
rather than 5–10 GB (D-005), and `fio`/NFS test cases are blocked (D-010).

## 11. How to reproduce

```bash
git clone <this repository>
cd minio-vs-silo-evaluation

# Credentials: copy the template and set synthetic lab values
cp lab/compose/.env.example lab/compose/.env
$EDITOR lab/compose/.env          # set MINIO_ROOT_USER and MINIO_ROOT_PASSWORD

# Images. The pinned images pull; the two locally built ones are rebuilt by:
./tools/bin/build-minio.sh       # needs tools/go and tools/src/minio
docker build -t mc-local:RELEASE.2025-08-13T08-35-41Z lab/images/mc

# Secret scanning
./tools/bin/install-hooks

# Lab, then evidence
./tools/bin/lab network
./tools/bin/lab up minio && ./tools/bin/lab up proxy
./tools/bin/st01-verify minio
```

Expected: four MinIO containers healthy, `lb-minio` healthy on
`127.0.0.1:18080`, and sixteen evidence files written under `evidence/`.

Every image is pinned by digest, so a rebuild on a clean host produces the same
binaries. The MinIO build is deterministic given the same source commit and Go
toolchain: the provenance file records all three.

## 12. Cleanup

```bash
# Stop the lab. Note the product name is always explicit.
./tools/bin/lab down minio
./tools/bin/lab down silo
./tools/bin/lab down proxy
./tools/bin/lab down workload

# Remove the shared network, once no lab container is attached
docker network rm migration-net

# Remove the client config volumes
docker volume rm mc-config silo-config
```

**`lab` never passes `-v` to `docker compose down`.** Cluster data lives in bind
mounts under `lab/data/`, which Compose does not own, so an accidental teardown
cannot destroy dataset evidence. Guardrails 20 requires this.

Removing `lab/data/` needs one extra step, because both servers write as root
inside the container and the host user cannot delete root-owned files (D-009):

```bash
# Run a throwaway root container over the bind mount
docker run --rm -v "$PWD/lab/data:/d" \
  registry.access.redhat.com/ubi9/ubi-micro@sha256:932aec77f5b86a5dba854a18b14a38725b296967e7dc9c7a1f4d7f0bf82e1ce5 \
  bash -c 'rm -rf /d/*'
```

A plain `rm -rf lab/data` by the invoking user will fail with permission errors.
That is expected, not a sign that the lab is still running.

**Pre-existing containers are not touched** by any of the above. `grafana`,
`cadvisor`, `soul-of-lahore` and `nginx-exporter` belong to unrelated stacks and
must remain running.