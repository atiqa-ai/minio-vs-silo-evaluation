# O01–O08 — Provisional Derivations

**Status: PROVISIONAL. These are not authoritative.**

The supplied SRD (`docs/00-srd/README.md`) refers to eight compatibility
conditions, O01–O08, and requires a written applies / does-not-apply decision with
supporting evidence for each. It does **not** define them. Section 7 names four of
them explicitly and points at a fifth by implication; for the remaining two the
supplied documents contain no basis at all.

This file records what each condition is taken to mean, how that reading was
derived, and how confident that reading is. It exists so that every later
`O0x — applies / does-not-apply` statement in this repository cites a visible
source rather than an invisible assumption.

**If the authoritative O01–O08 text becomes available, this file must be
replaced and every applicability decision that relied on it must be re-checked.**
The two entries with no basis in the documents (O05, O08) are the ones most
likely to change.

---

## Confidence legend

| Level | Meaning |
|---|---|
| **Explicit** | The SRD names this condition and describes its subject. |
| **Implied** | The SRD states a constraint that only one condition can correspond to. |
| **No basis** | Nothing in the supplied documents identifies what this condition covers. |

---

## O01 — Cluster homogeneity in distributed mode

**Confidence: Implied.**
**Source:** SRD section 7, "In distributed mode":

> All nodes must run the same product.
> All nodes must run the same version.
> MinIO and Silo cannot be mixed within one cluster.
> Compatibility must therefore be demonstrated test by test.

**Statement taken to mean.** A Silo deployment is compatible only if a cluster
behaves correctly when every node runs Silo at a single version, and migration is
only safe if it is performed per test rather than by mixing products inside a live
cluster. Nothing may be concluded from a cluster containing both products.

**Why this is inference rather than definition.** The SRD never labels this
constraint "O01". It is the only compatibility condition that a reader would
naturally assign to O01, since O02, O03 and O04 are named in the very next
paragraph, which leaves O01 as the condition for the constraint stated above it.

**Verification implication.** Directly enforced in the lab:
`tools/bin/check-no-mixed-cluster` runs as a pre-commit hook and rejects any
Compose project or nginx upstream block that references both products. Evidence:
`docs/01-repository-and-lab/evidence/`.

---

## O02 — Custom authorization policy behavior

**Confidence: Explicit.**
**Source:** SRD section 7, "Special attention is required for: O02 — custom
authorization policy behavior".

**Statement taken to mean.** IAM policies with custom action and resource
elements must behave identically on MinIO and Silo — including wildcard actions,
resource ARNs with path components, deny-by-default behaviour, and whether an
authorised action is refused when a related action is not granted.

**Verification implication.** Covered by the ST07 policy test cases; requires
evidence per policy, not a single aggregate result.

---

## O03 — Older authentication and notification settings

**Confidence: Explicit.**
**Source:** SRD section 7, "O03 — older authentication and notification settings".

**Statement taken to mean.** Configuration written for an older MinIO release must
still be honoured: legacy authentication settings, and legacy bucket-notification
configuration (the pre-ARN, pre-`sqs`/`webhook` identifier forms, and the
`MINIO_NOTIFY_*` environment form).

**Verification implication.** Two distinct subjects in one condition. They should
be reported as separate sub-results (O03a authentication, O03b notification)
rather than a single pass/fail, because a failure in one says nothing about the
other.

---

## O04 — Programs relying on old bugs

**Confidence: Explicit.**
**Source:** SRD section 7, "O04 — programs relying on old bugs".

**Statement taken to mean.** Some deployed applications depend on MinIO
behaviours that are bugs. Silo fixing such a bug is a compatibility break even
though it is a correctness improvement. The evaluation must identify
bug-dependency in the specific workload under assessment, and report any case
where Silo differs from MinIO specifically because a bug was fixed.

**Verification implication.** This condition cannot be answered in the abstract.
It requires knowing what the target applications do. Until that is established,
the honest result is "not applicable — workload unknown", and that answer must be
recorded as such rather than passed.

---

## O05 — *(no basis found)*

**Confidence: No basis.**

The supplied SRD names O02, O03, O04, O06 and O07. It gives no subject for O05.
No sentence in `docs/00-srd/README.md` or `docs/00-srd/project-context.md` maps
onto it that is not already claimed by another condition.

**Candidate readings, none supported by the documents:**

- Core S3 API surface compatibility (the most plausible, since it is the bulk of
  ST05/ST06 and the obvious first condition in such a list).
- Object versioning and object-lock behaviour.
- Encryption and KMS/TLS configuration behaviour.

**How this is handled.** Until the authoritative text is available, O05 is
treated as **not assessed**, and this is stated as a gap in the compatibility
assessment rather than being quietly resolved by picking the most plausible
candidate. Claiming an applies/does-not-apply decision for O05 on the basis of a
guess would be the exact failure mode the evidence rules exist to prevent.

---

## O06 — Multi-pool behaviour

**Confidence: Explicit.**
**Source:** SRD section 7, "O06/O07 — multi-pool, replication and mixed-version
behavior". The shared phrase names multi-pool first, so it is attributed to O06.

**Statement taken to mean.** A cluster configured with more than one erasure pool
and set topology must behave correctly: pool and set counts are honoured, objects
are placed and reported in the correct pool, and health reporting is accurate.

**Note on scope.** The lab topology for this evaluation is a single pool with
four drives in one set, which is what SRD Profile B specifies. A multi-pool
cluster is therefore **out of scope for the lab as built**, and O06 can only be
assessed as not-applicable-in-this-configuration unless a multi-pool cluster is
deliberately built. That limit must be stated in the compatibility assessment.

---

## O07 — Replication and mixed-version behaviour

**Confidence: Explicit.**
**Source:** SRD section 7, same shared phrase: "multi-pool, replication and
mixed-version behavior".

**Statement taken to mean.** Replication targets and mixed-version behaviour must
be characterised: whether a Silo cluster can replicate to a MinIO cluster and
vice versa, and what happens when versions differ within a replication
relationship.

**Note on scope.** Replication in this evaluation is deliberately NOT set up.
Guardrails 11 prohibits live data movement between the two products, because data
integrity results must be reproducible in both directions without one product
having operated on the other's objects. Replication is a live data path between
products, so setting it up would breach that guardrail. O07 must therefore be
assessed as blocked by design, with the guardrail citation given, rather than
tested.

---

## O08 — *(no basis found)*

**Confidence: No basis.**

Like O05, O08 is named in the condition list but never given a subject anywhere in
the supplied documents.

**Candidate readings, none supported by the documents:**

- Operational concerns: upgrade procedure, backup and restore, monitoring hooks.
- Licensing and maintenance posture (SRD objective 7 covers security, licensing
  and maintenance, which is close in subject matter).
- Notification and event destinations beyond the legacy forms in O03.

**How this is handled.** Same as O05: treated as **not assessed** pending the
authoritative text, and reported as a gap.

---

## Summary

| ID | Subject | Confidence | Covered by lab test cases |
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

Two of eight conditions cannot be assessed at all from the supplied documents.
That is recorded here so the final recommendation can state it plainly rather than
implying full O01–O08 coverage.