# Environment block — required versus actual

Copy this block into the environment section of **every** phase write-up. It
exists because R1/R3 found the gap between what the SRD requires and what this
host provides was being described in prose, where it is easy to overstate.

## How to use this template

1. Copy the whole block into the phase document under a heading like
   `### Environment — required versus actual`.
2. Fill every **Actual** cell with a measured value, not an estimate. Run the
   command shown and paste the output into the evidence file.
3. Delete any row that does not apply to the phase. Do not delete a row because
   it is inconvenient — an unmet requirement is a result.
4. Set **Overall** to `Indicative only` if any row is `Not met`. Do not soften
   this. The point of the block is that a reader sees the gap immediately.
5. If a required item genuinely cannot be met, record it here **and** raise a
   deviation in `DEVIATIONS.md`. An unmet requirement with no deviation is an
   undocumented gap.

## Terminology

The environment is the **Approved Controlled Reduced-Resource Execution
Environment**. It is not Profile A or Profile B compliant, and no new profile
name may be introduced. `tools/bin/check-env-claims` enforces this on every
commit, so an invented profile name will fail the pre-commit hook.

---

## Environment — required versus actual

**Phase:** `<DEV-9xx>`
**Date (UTC):** `<YYYY-MM-DDTHH:MM:SSZ>`
**Host:** `<hostname>`
**Execution environment:** Approved Controlled Reduced-Resource Execution
Environment

### Hardware and platform

| Item | Required (SRD reference) | Actual (measured) | Met? | Evidence |
|---|---|---|---|---|
| vCPU | `<n>` | `<n>` — `nproc` | Yes / No / **Not met** | `<file>` |
| RAM | `<n>` GiB | `<n>` GiB — `free -g` | Yes / No / **Not met** | `<file>` |
| Disk | `<n>` GB | `<n>` GB total, `<n>` GB free — `df -h /` | Yes / No / **Not met** | `<file>` |
| Filesystem | `<type>` | `<type>` | Yes / No | `<file>` |
| Virtualisation | bare metal | `<VMware guest>` (D-019) | Approved deviation | `<file>` |

### Software

| Item | Required | Actual (with version) | Met? | Evidence |
|---|---|---|---|---|
| OS | `<distro> <version>` | `<uname -a>` | Yes / No | `<file>` |
| Docker | `<version>` | `<version>` | Yes / No | `<file>` |
| Go | `<version>` | `<version>` | Yes / No | `<file>` |

### Product under test

Record **one row per product**. Never a combined row — that is what the
Identical-Test Rule forbids.

| Product | Version | Image reference (pinned) | Image digest | Evidence |
|---|---|---|---|---|
| MinIO | `<version>` | `<repo>:<tag>` | `sha256:<digest>` | `<file>` |
| Silo | `<version>` | `<repo>:<tag>` | `sha256:<digest>` | `<file>` |

### Storage and dataset

| Item | Required | Actual | Met? | Evidence |
|---|---|---|---|---|
| Dataset profile | `<profileb / reduced2g / reduced1g>` | `<profile>` | Yes / No | `<file>` |
| Object count | `<n>` | `<n>` | Yes / No | `<file>` |
| Total bytes | `<n>` | `<n>` | Yes / No | `<file>` |
| Profile B floor (5 GiB) | 5 GiB | `<n>` GiB | Yes / No | `<file>` |

### Tooling

| Tool | Required | Actual (version + SHA-256) | Met? | Evidence |
|---|---|---|---|---|
| `mc` | same for both products | `<version>` `<sha256>` | Yes / No | `<file>` |
| `mcli` | secondary only | `<version>` `<sha256>` | Yes / No | `<file>` |
| `fio` | `<version>` | `<version>` | Yes / No | `<file>` |

Record the versions of **both** clients every time. R15: Silo ships its own
client symlinked as `mc`, so an unrecorded client makes the comparison
meaningless.

### Requirements this environment prevented

State each one plainly, with the reason. Do not convert an unmet requirement
into a soft finding.

| Requirement | Why it could not be met | How it is handled instead |
|---|---|---|
| `<requirement>` | `<technical reason>` | Not Available, with this reason / indicative only |

### Overall

**Indicative only.** `<n>` of `<m>` required items are unmet: `<list>`.

Results from this phase are indicative and do not establish Profile A or
Profile B performance. See `DEVIATIONS.md` D-019.