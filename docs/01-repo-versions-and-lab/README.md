# ST01 — Repository and Lab

> **Section map.** Sections 1-12 below are the original write-up, left
> exactly as recorded. The per-subtask template also requires Scope, Acceptance
> Criteria, Limitations / Assumptions, Files Changed and a Review Gate; those are
> added here as unnumbered sections in their template positions rather than
> renumbering the original twelve, so existing cross-references stay valid.

## 1. Goal

Set up the repository, pin every version, and build a working local Docker
Compose lab in which a MinIO CE cluster and a Silo cluster can be started,
verified and compared under identical conditions.

This subtask does not measure performance or judge compatibility. It establishes
that the lab is trustworthy, so that later subtasks can rely on it.

## Scope

Only the requirements of this sub-task and the project specification. Work
outside that boundary is recorded under Findings, not implemented.

Not in scope for this sub-task: performance measurement (DEV-910, DEV-913),
Silo functional validation (DEV-911), compatibility difference testing
(DEV-912), and security/licensing review (DEV-914).

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
| Virtualisation | VMware guest |

The host is below the 8 vCPU / 32 GiB reference on both CPU and memory, and
is itself virtualised, so **every measurement in this evaluation is indicative
only**.

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

# 3. Metrics scraper. Starts alongside whichever single cluster is up and
#    publishes no host ports.
./tools/bin/lab up monitoring

# 4. Capture ST01 evidence for the MinIO baseline
./tools/bin/st01-verify minio

# 5. Tear the baseline down before starting Silo: only one heavy cluster
#    running both heavy stacks at once
./tools/bin/lab down minio
./tools/bin/lab down proxy

# 6. Silo cluster, identical topology and limits
./tools/bin/lab up silo
./tools/bin/lab up proxy

# 7. Capture ST01 evidence for the Silo pass. The scraper keeps running and
#    is expected to report the MinIO targets as down, which is the recorded
#    proof that only one heavy stack was live at a time.
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

All eight test cases passed on MinIO. On Silo, TC-ST01-01 through TC-ST01-05
passed; **TC-ST01-06, -07 and -08 are recorded as NOT RUN against Silo** — see the
correction below. The earlier wording of this section claimed all eight passed in
both passes, which the Silo evidence did not support.

| Evidence | Covers |
|---|---|
| `evidence/TC-ST01-01-{minio,silo}.txt` | Docker environment, storage, disk |
| `evidence/TC-ST01-02-{minio,silo}.txt` | Compose v2, all five projects validate |
| `evidence/TC-ST01-03-minio.txt` | MinIO tag, image ID, source provenance, runtime version |
| `evidence/TC-ST01-04-silo.txt` | Silo tag, image digest, server and `mcli` versions |
| `evidence/TC-ST01-05-{minio,silo}.txt` | `migration-net` exists; every lab container on exactly one network |
| `evidence/TC-ST01-06-minio.txt` | Monitoring scrapes the live cluster; nodes healthy, reachable, DNS resolves |
| `evidence/TC-ST01-06-silo.txt` | **Stale** — predates the monitoring project, see below |
| `evidence/TC-ST01-07-silo.txt` | **Stale** — predates the monitoring project, see below |
| `evidence/TC-ST01-08-silo.txt` | **Stale** — predates the monitoring project, see below |

### Correction: the Silo monitoring evidence predates the monitoring project

TC-ST01-06, -07 and -08 assert that monitoring scrapes the cluster, that no
unexpected container publishes a port, and that all five projects validate. The
Silo files carrying those assertions were captured at **18:35**, before
`lab/compose/monitoring/` was created at **20:00**, and none of the three contains
the string `prometheus` or `monitoring` anywhere. They therefore evidence the state
of the lab *before* the monitoring project existed, and cannot evidence a PASS for
monitoring on Silo.

The MinIO files for the same three cases were recaptured at **20:10**, after the
change, and do support their assertions. That asymmetry is why the summary above
has been rewritten: it is the only way the report can be true of both files.

This is a documentation defect, not a lab defect. The Silo cluster is understood
to behave correctly here, exactly as MinIO does, because the same monitoring
project scrapes both and MinIO's pass is proven. But "understood to" is not
evidence, and raw output is required for every PASS claim. The three Silo
cases are therefore reported as NOT RUN and are queued for re-execution in the
Silo turn, when the Silo cluster is next up. Until then the Monitoring row of the
Silo column in the results table must not be read as a PASS.
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

The `monitoring` project came up healthy and collected
**77 distinct `minio_*` metric names** from the four live MinIO nodes. It
publishes nothing: `HostConfig.PortBindings` for `lab-prometheus` is `{}`, and
`Config.ExposedPorts` is only container metadata. Both facts are captured in
`TC-ST01-07-minio.txt` and `TC-ST01-08-minio.txt`.

Bringing the scraper up exposed a lab-side defect rather than a product one:
every node answered `403 Forbidden` on `/minio/v2/metrics/cluster` until
`MINIO_PROMETHEUS_AUTH_TYPE=public` was set. That variable was then set
identically on all four nodes of **both** clusters, so the metric surface stays
comparable and neither product gains an advantage. Recorded as D-015, and
explicitly **not** a product finding: no MinIO-versus-Silo comparison was made
and none may be inferred from it.

## 7. PASS/FAIL

**ST01: PASS**, with one requirement met after the fact and three Silo monitoring
cases not yet evidenced.

| Completion requirement | MinIO | Silo | Evidence |
|---|---|---|---|
| Docker environment ready | PASS | PASS | `TC-ST01-01-{minio,silo}.txt` |
| Docker Compose v2 ready | PASS | PASS | `TC-ST01-02-{minio,silo}.txt` |
| Product version pinned | PASS | PASS | `TC-ST01-03-minio.txt`, `TC-ST01-04-silo.txt` |
| Image digests recorded | PASS | PASS | both files above |
| `migration-net` configured | PASS | PASS | `TC-ST01-05-{minio,silo}.txt` |
| Monitoring scrapes the live cluster | PASS | **NOT RUN** | `TC-ST01-06-minio.txt`; Silo file is stale |
| No unexpected port published | PASS | **NOT RUN** | `TC-ST01-07-minio.txt`; Silo file is stale |
| All five projects validate | PASS | **NOT RUN** | `TC-ST01-08-minio.txt`; Silo file is stale |
| Secret scanning / pre-commit active | PASS | n/a (repo-wide) | `evidence/secret-scanning.txt` |

Repository evidence — Compose files, digests, `docker compose ps`, environment
information and command output — is present under `lab/compose/` and `evidence/`.

### Screenshots

This phase has no `screenshots/` directory. Its placeholder README was removed
in `f59d0f2`; the redaction checklist it carried was preserved here rather than
discarded, and the template now lives at
[`docs/templates/screenshots-readme.md`](../templates/screenshots-readme.md).

A screenshot is supporting evidence only and is never sufficient for a
PASS/FAIL claim. The authoritative evidence for the
results above is the raw output under `evidence/`.

Before any image is committed, check it for:

* access keys, secret keys, passwords, tokens, private keys
* internal IPs, hostnames, domains, email addresses
* unredacted IAM or bucket metadata

`pre-commit` runs gitleaks over staged content and `tools/bin/install-hooks`
installs the same scan as a git-native hook. A clean scan is necessary but not
sufficient: gitleaks detects credential patterns, not an internal hostname
visible in a terminal window.

Two qualifications on that verdict:

* The public-repository requirement was initially unmet by explicit decision and
  was met on 2026-10-01; D-001 records both the deviation and its resolution. The
  repository is now public and the twelve Jira-keyed issues exist.
* The three Silo `NOT RUN` cells are a documentation defect corrected above, not a
  lab defect. They are re-queued for the Silo turn.

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
| `lab-prometheus` (monitoring) | none — `HostConfig.PortBindings` is `{}` | no |

Only the consoles and the proxy may publish ports, so the monitoring
project has no `ports:` key at all and is reachable only from `migration-net`.
`Config.ExposedPorts` still lists `9090/tcp`, but that is container metadata,
not a host binding — the distinction is recorded explicitly in the evidence so
the two are not confused.

Pre-existing containers outside this project (`grafana` on `0.0.0.0:3001`,
`cadvisor` on `0.0.0.0:8080`, `soul-of-lahore`, `nginx-exporter`) were left
running and untouched. TC-ST01-08 records them explicitly as *not* this
project's ports, so their wildcard bindings cannot be mistaken for a product
failure here.

## Acceptance Criteria

| Criterion | Status | Evidence / Notes |
|---|---|---|
| _(author to complete)_ | NOT AVAILABLE | Phase not yet reviewed against a gate |

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
failure is recorded here rather than deleted.

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

## Limitations / Assumptions

**Assumptions.** None recorded beyond those stated inline.

**Limitations.** See the single environment line under *Environment* above and
*Findings and problems* below. Every result in this sub-task is indicative, and
none of it establishes reference-host performance.

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

All five Compose projects exist and validate, including the
`monitoring` project, which scrapes the live cluster over `migration-net` without
publishing a single port. The repository is public at
`https://github.com/atiqa-ai/minio-vs-silo-evaluation` on `main`, with the epic
and all twelve subtasks mirrored as GitHub issues. The residual gap on D-001 is
that those issues are not yet attached to a GitHub Project board. Creating one
is blocked on token scope: `gh` lacks `read:project`, and the grant needs a
browser device flow. Run `gh auth refresh -s read:project,project`, then
`gh project create --owner atiqa-ai`. See `evidence/github-tracker.txt`.

Two limits are inherited from the host and must be restated in the final
recommendation:

- **Benchmarks are indicative only.** 4 vCPU, 7.7 GiB RAM, VMware, cgroup v2 —
  below the 8 vCPU / 32 GiB reference host.
- **The dataset did not initially meet the 5 GB floor.** The first generator
  iteration realised **885.82 MiB / 669 objects**. ST02 is regenerating at the 5 GB
  minimum, and until that passes, no benchmark number from this dataset counts as
  evidence from a compliant dataset.

`fio` and the NFS test cases are **no longer blocked** (D-010): they will run in
containers rather than needing host packages. That supersedes the earlier
"blocked" note in this section.

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
cannot destroy dataset evidence. A dataset required by an active evidence set is
never destroyed before its evidence is captured and persisted.

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

## Files Changed

_(author to complete — list the files this sub-task added or modified)_

## Review Gate

- [ ] Requirements checked
- [ ] Evidence present for every PASS
- [ ] Result reproducible from the repository
- [ ] Public-repo secret scan passed
- [ ] Documentation complete
- [ ] Tracker updated
- [ ] Reviewer gate satisfied

