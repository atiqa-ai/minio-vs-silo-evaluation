# Screenshots directory README — template

Copy this into `docs/<phase>/screenshots/README.md` when a phase is first set
up. It exists so the required per-subtask folder structure is present in the
repository even when no screenshot is yet warranted.

**A screenshot is supporting evidence only. A screenshot alone is never
sufficient evidence for a PASS/FAIL claim.** The authoritative evidence for a
result is the raw command output in `../evidence/`.

## Before committing any image

Each image must be checked for the following before it is committed:

* access keys, secret keys, passwords, tokens, private keys
* internal IPs, hostnames, domains, email addresses
* unredacted IAM or bucket metadata

`pre-commit` runs a gitleaks secret scan over staged content, and
`tools/bin/install-hooks` installs the same scan as a git-native hook so it also
runs without the pre-commit framework. A scan pass is necessary but not
sufficient: gitleaks detects credential patterns, not an internal hostname
printed in a terminal window.

## Recording the image

Any image placed here must be listed in the phase README's results table with
the reason it was needed. A screenshot with no stated reason is not evidence, it
is noise.

## Naming

`<test-id>-<short-description>.png`, for example
`TC-ST01-01-minio-dashboard.png`. The test id must match the entry in the
phase README and the file in `../evidence/`.

## Note on removal

The owner removed the phase-01 placeholder in `f59d0f2` as repo clutter. The
redaction checklist was preserved by moving it into the phase README and into
this template, so deleting a placeholder no longer discards the guidance. If
these placeholders are removed across all phases, use this template whenever a
phase genuinely needs a `screenshots/` directory.