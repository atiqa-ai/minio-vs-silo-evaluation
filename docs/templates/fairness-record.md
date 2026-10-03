# Fairness record — one client drives both products

Copy this into the evidence directory of **every** phase that runs a client
against either product. R15 exists because Silo ships a binary symlinked as
`mc`, which invites the silent substitution of two different clients for two
different products. That produces a comparison of the clients rather than of
the servers. Comparisons must use identical machine, topology, limits, storage,
dataset, benchmark profile, repetitions and measurement approach.

The rule is structural, not a matter of intent: **the same client binary drives
both products.** MinIO's `mc` is the primary client for both.

## The rule

| Product | Primary client | Allowed? |
|---|---|---|
| MinIO | MinIO `mc` | Yes |
| Silo | MinIO `mc` | Yes — **required**, this is the point |
| MinIO | Silo `mcli` | Only where `mcli` is the sole option, and recorded as a DEV-912 compatibility finding |
| Silo | Silo `mcli` | Only where `mcli` is the sole option, and recorded as a DEV-912 compatibility finding |

Any behaviour that differs between `mc` and `mcli` against the same endpoint is
a **compatibility finding about the products**, not a tooling artefact. Record
it under DEV-912; do not resolve it by switching clients.

---

# Fairness record

**Phase:** `<DEV-9xx>`
**Date (UTC):** `<YYYY-MM-DDTHH:MM:SSZ>`

## Client binaries used

Record the exact binary and its checksum for every client invoked. A version
string alone is not sufficient — `mcli` is extracted from a container image and
must be traceable to that image.

| Role | Binary | Path | Version | SHA-256 | Source |
|---|---|---|---|---|---|
| Primary (both products) | `mc` | `<path>` | `<version>` | `<sha256>` | `<extracted from / repo>` |
| Secondary | `mcli` | `<path>` | `<version>` | `<sha256>` | extracted from `<repo>@sha256:<digest>` |

### Provenance

| Item | Value |
|---|---|
| `mcli` source image | `<repo>:<tag>` |
| `mcli` source image digest | `sha256:<digest>` |
| Silo release commit | `<commit>` |

## Commands run

The commands must be identical apart from the endpoint. Show them verbatim;
this is what makes the comparison auditable.

```bash
# Against MinIO
<command using mc against minio endpoint>

# Against Silo
<command using mc against silo endpoint>
```

If any command differs beyond the endpoint, record why in the next section.

## Deviations from identical commands

| # | Product | What differed | Why | Why `mc` could not be used | Recorded as |
|---|---|---|---|---|---|
| 1 | `<product>` | `<difference>` | `<reason>` | `<reason>` | DEV-912 finding `<id>` / tooling note |

An empty table is the expected and desired result.

## Identical configuration

Both products must be configured the same way, or the comparison measures the
configuration.

| Setting | MinIO | Silo | Identical? |
|---|---|---|---|
| Node count | `<n>` | `<n>` | Yes / **No** |
| Drives per node | `<n>` | `<n>` | Yes / **No** |
| CPU limit | `<value>` | `<value>` | Yes / **No** |
| Memory limit | `<value>` | `<value>` | Yes / **No** |
| Volume type | `<type>` | `<type>` | Yes / **No** |
| Dataset profile | `<profile>` | `<profile>` | Yes / **No** |
| TLS | `<state>` | `<state>` | Yes / **No** |

Any `No` is a finding. `tools/bin/check-no-mixed-cluster` enforces the node
separation mechanically; this table records that the rest matched.

## Verdict

- [ ] One client binary drove both products.
- [ ] Both client versions and checksums are recorded above.
- [ ] Every differing command is listed with a reason.
- [ ] Both products had identical node count, drives, limits, and dataset.

If any box is unticked, the phase comparison is **not** a like-for-like result
and must be labelled as such in the phase write-up.