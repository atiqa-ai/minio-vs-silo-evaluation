# Environment block — required versus actual

Copy this block into the environment section of **every** phase write-up.

The purpose is narrow: a reader must be able to see, at a glance, the gap
between what a result assumes and what the host actually provided. Prose hides
that gap; a table does not.

## How to use this template

1. Copy the block into the phase document under `### Environment`.
2. Fill every **Actual** cell with a measured value, not an estimate. Run the
   command shown and paste the output into the evidence file.
3. Delete rows that genuinely do not apply. Do not delete a row because it is
   inconvenient — an unmet requirement is itself a result.
4. Keep **Overall** as `Indicative only` if any row reads `Not met`. Do not
   soften it.
5. If something could not be met for a technical reason, record it under
   *Constraints on these results* and add an entry to `DEVIATIONS.md`. An unmet
   requirement with no record is an undocumented gap.

## Terminology

State the host as it is. Use measured values and the reference figures they are
compared against. Two specific claims are checked on every commit by
`tools/bin/check-env-claims`:

* **No invented profile names.** Only the profiles the project defines may be
  named; a name that does not exist is fabrication once it is written down.
* **No unsupported compliance claims.** Do not assert that results meet a
  reference configuration. The honest form is "below the reference" plus the
  measured figure.

---

## Environment — required versus actual

**Phase:** `<DEV-9xx>`
**Date (UTC):** `<YYYY-MM-DDTHH:MM:SSZ>`
**Host:** `<hostname>`

Results in this phase were produced on a VMware guest with 4 vCPU and
approximately 7.7 GiB of RAM, below the 8 vCPU / 32 GiB reference. They are
indicative.

### Hardware and platform

| Item | Reference | Actual (measured) | Met? | Evidence |
|---|---|---|---|---|
| vCPU | `<n>` | `<n>` — `nproc` | Yes / **No** | `<file>` |
| RAM | `<n>` GiB | `<n>` GiB — `free -g` | Yes / **No** | `<file>` |
| Disk | `<n>` GB | `<n>` GB total, `<n>` GB free — `df -h /` | Yes / **No** | `<file>` |
| Filesystem | `<type>` | `<type>` | Yes / No | `<file>` |
| Virtualisation | `<bare metal / any>` | `<VMware guest>` | No | `<file>` |

### Software

| Item | Reference | Actual (with version) | Met? | Evidence |
|---|---|---|---|---|
| OS | `<distro> <version>` | `<uname -a>` | Yes / No | `<file>` |
| Docker | `<version>` | `<version>` | Yes / No | `<file>` |
| Go | `<version>` | `<version>` | Yes / No | `<file>` |

### Product under test

Record **one row per product**. Never a combined row — that is what makes an
identical comparison meaningless.

| Product | Version | Image reference (pinned) | Image digest | Evidence |
|---|---|---|---|---|
| MinIO | `<version>` | `<repo>:<tag>` | `sha256:<digest>` | `<file>` |
| Silo | `<version>` | `<repo>:<tag>` | `sha256:<digest>` | `<file>` |

### Storage and dataset

| Item | Required | Actual | Met? | Evidence |
|---|---|---|---|---|
| Dataset profile | `<profile name>` | `<profile name>` | Yes / No | `<file>` |
| Object count | `<n>` | `<n>` | Yes / No | `<file>` |
| Total bytes | `<n>` | `<n>` | Yes / No | `<file>` |
| Dataset floor | `<n>` GiB | `<n>` GiB | Yes / No | `<file>` |

### Tooling

| Tool | Required | Actual (version + SHA-256) | Met? | Evidence |
|---|---|---|---|---|
| `mc` | same for both products | `<version>` `<sha256>` | Yes / No | `<file>` |
| `mcli` | secondary only | `<version>` `<sha256>` | Yes / No | `<file>` |
| `fio` | `<version>` | `<version>` | Yes / No | `<file>` |

Record both client versions every time. Silo ships its own client, so an
unrecorded client makes the comparison meaningless.

### Constraints on these results

State each one plainly, with the technical reason. Do not convert an unmet
requirement into a soft finding.

| Constraint | Why | How it is handled instead |
|---|---|---|
| `<constraint>` | `<technical reason>` | NOT AVAILABLE with this reason / indicative only |

### Overall

**Indicative only.** `<n>` of `<m>` required items are unmet: `<list>`.

Results from this phase do not establish reference-host performance.