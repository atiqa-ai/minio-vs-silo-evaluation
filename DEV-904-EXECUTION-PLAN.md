# DEV-904 — Master Execution Plan

**Epic:** DEV-904 — MinIO vs Silo evaluation
**Plan date:** 2026-10-03
**Plan status:** Approved for execution, DEV-905 authorised
**Governing documents:** `SRD`, `PROJECT_GUARDRAILS`, `AGENTIC_EXECUTION_PROTOCOL`, `EVIDENCE_GUIDE`, `FINAL_PROJECT_QA_CHECKLIST`

Every departure from a requirement is recorded in [`DEVIATIONS.md`](DEVIATIONS.md).
This plan does not restate requirements it intends to satisfy; it states how the work
is sequenced, gated and evidenced.

---

## 1. Objective

Establish, with reproducible evidence, whether Silo is a safe drop-in replacement for
the last open-source MinIO, and produce a go/no-go recommendation backed by
reproducible measurements rather than inference.

Success is not "the comparison ran". Success is that a reader can re-run any claim,
see the same result, and see the required-versus-actual gap where the environment
prevented the requirement being met.

## 2. Sources

| Source | Role | Authority |
|---|---|---|
| SRD | Scope, profiles A/B, phases, DoD, test cases | Normative for requirements |
| Project guardrails | Prohibitions: VMs, mixed clusters, destructive commands, unevidenced claims | Normative, overrides convenience |
| Agentic execution protocol | Startup, command safety, commit discipline, stop conditions | Normative for process |
| Evidence guide | Evidence hierarchy, naming, capture, sanitisation | Normative for evidence |
| Phase plan | Phase order and gates | Normative for sequence |
| Final QA checklist | Epic sign-off | Normative for closure |
| Silo compatibility documentation | O01–O08 condition text | **Vendor claim.** Authoritative for the wording; not authoritative for the behaviour, which we test |
| Upstream MinIO documentation | Expected MinIO behaviour | Reference, dated on retrieval |

SRD and guardrails win over vendor documentation, which wins over anything inferred.
Where sources conflict, the conflict is recorded in `DEVIATIONS.md` rather than
resolved silently.

## 3. Constraints

**Binding, non-negotiable:**

- Phases execute strictly `DEV-905 → … → DEV-915`. One authorised phase at a time.
- No MinIO and Silo nodes in the same cluster. Enforced by pre-commit hook.
- No destructive host or container command without recorded authorisation and
  before/after state.
- No credentials, internal hostnames, domains or addresses in a public repository.
- No result without captured raw output. No inference presented as measurement.
- Failures, including failures of the lab itself, stay in the record.
- Synthetic data only.
- Images pinned by tag and digest.

**Execution-environment constraint.** All work executes in an Approved Controlled
Reduced-Resource Execution Environment: VMware guest, 4 vCPU, ~7.7 GB RAM, single
48 GB filesystem, against the Profile B reference of 8 vCPU / 32 GB recorded in
`DEVIATIONS.md` D-004. The authoritative profile figures are held in the external
project requirements and are not restated in this plan. VMware and the reduced
resources are approved conditions. Profile A and Profile B requirements are
**unchanged**. The gap is an approved deviation recorded in `DEVIATIONS.md` D-019, not
a new profile and not a silent downgrade. No artefact may state that Profile A or
Profile B was completed.

**Scope exclusions.** Production data, real customer workloads, live migration,
application-level integration testing, and TCO modelling are out of scope and are
recorded in `OUT_OF_SCOPE.md` rather than silently dropped.

## 4. Phase plan

Each phase lists its goal, gate, and the state it must leave the lab in. Detailed
per-test procedures are authored in the phase's own `docs/NN-*/README.md` at the time
the phase runs, not in advance, so that expected results are written before
observation rather than reconstructed after it.

### DEV-905 — Repository, versions, single-node lab
**Goal.** Pin every version by tag and digest, assess the host, build a MinIO
single-node Compose lab with TLS, add basic monitoring, and establish the test matrix.
**Actions.** Restore and migrate documentation to the phase structure; promote
governance documents to repository root; record the controlled environment; build
`fio` and NFS environments; extract and pin `mcli`; establish the port allocation;
reclaim disk under recorded authorisation; re-run secret scanning over the working
tree **and Git history**.
**Gate.** Every acceptance criterion evidenced; controlled environment documented
against all required items; re-baselined lab reproducible from the repository alone.
**Lab state.** Single-node MinIO running, monitoring scraping it.

### DEV-906 — Dataset, fixtures, manifest tooling
**Goal.** Generate the synthetic dataset, create versioning/object-lock/lifecycle/IAM
fixtures, and provide manifest generation plus comparison tooling.
**Actions.** Add reduced dataset profiles without resizing existing ones; regenerate
the lost server-side capture; fix the multipart ETag handling defect; verify against
deliberately altered, deleted and missing objects.
**Gate.** Every required dataset category present; deliberately introduced manifest
differences detected; ground-truth manifest committed and reproducible.
**Lab state.** Dataset generated, manifest tooling proven by negative control.

### DEV-907 — MinIO single-node feature validation
**Goal.** Validate the MinIO feature set in single-node mode.
**Actions.** Test each listed feature with expected result recorded first; capture
raw output per test case.
**Gate.** Every feature has expected/observed result and evidence.
**Lab state.** Feature matrix complete for single node. Supersedes the earlier
distributed-mode execution of this phase; see D-013 supersession.

### DEV-908 — MinIO distributed mode
**Goal.** Validate distributed mode, resilience, healing and expansion.
**Actions.** Multi-node deployment; drive node and network failures; observe healing;
verify data against the manifest; test rolling restart and expansion.
**Gate.** Failure, heal and expansion evidence plus manifest verification complete.
**Lab state.** Cluster healed and verified against ground truth.

### DEV-909 — MinIO replication
**Goal.** Validate bucket, batch and site replication and produce the runbook.
**Actions.** Two concurrent MinIO deployments; each replication mode; failure
recovery; replication lag measurement; manifest verification on the target.
**Gate.** Replication modes, failure recovery, lag and manifest verification complete.
**Lab state.** Replication verified, runbook written. MinIO-only co-residency;
see the phase note in `docs/05-minio-replication/README.md`.

### DEV-910 — MinIO performance baseline
**Goal.** Establish the MinIO performance baseline.
**Actions.** Run the required `warp` profiles at reduced parameters with the
reduction documented; storage-layer `fio` measurements; repeated runs with variance.
**Gate.** All required measurements complete with repetitions and variance reported.
**Lab state.** Baseline captured and reproducible.

### DEV-911 — Silo functional validation
**Goal.** Validate Silo functionally in an environment comparable to DEV-907.
**Actions.** Re-run the applicable DEV-907 tests against Silo with the same client,
dataset, scripts and parameters; place every Silo result beside its MinIO counterpart.
**Gate.** Silo result beside every MinIO result.
**Lab state.** Functional parity table complete.

### DEV-912 — Compatibility edge cases and O01–O08
**Goal.** Establish where the two products differ in ways a migration would notice.
**Actions.** Capture the authoritative O01–O08 text with URL and retrieval date;
record an applies / does-not-apply decision per condition with evidence; test S3 and
client edge cases.
**Gate.** Every O-condition has an evidence-backed decision.
**Lab state.** Compatibility difference matrix complete.

### DEV-913 — Silo performance comparison
**Goal.** Compare Silo performance against the MinIO baseline.
**Actions.** Identical benchmark methodology, identical reduced parameters, same
client; side-by-side deltas with variance.
**Gate.** Identical methodology and side-by-side deltas.
**Lab state.** Comparison complete, labelled indicative.

### DEV-914 — Security, licensing, maintenance
**Goal.** Assess security, licensing and maintenance risk.
**Actions.** CVE and vulnerability table with retrieval dates; image and binary
provenance; licence obligations including Silo's AGPL terms; maintenance and fork
sustainability; exit strategy.
**Gate.** CVE table, provenance, licence review, maintenance risk and exit strategy.
**Lab state.** Documentation only.

### DEV-915 — Capability matrix and recommendation
**Goal.** Produce the decision the Epic exists to deliver.
**Actions.** Capability matrix from evidenced results only; executive report; risks
and open questions; go/no-go recommendation with conditions.
**Gate.** Mentor review and decision recorded.
**Lab state.** Final report set.

## 5. Dependencies

```text
DEV-905 ──> DEV-906 ──> DEV-907 ──> DEV-908 ──> DEV-909 ──> DEV-910
                                                              │
   FINAL_PROJECT_QA_CHECKLIST <── DEV-915 <── DEV-914 <── DEV-913 <── DEV-912 <── DEV-911
```

- DEV-906 requires DEV-905: no dataset work without a pinned, running lab.
- DEV-907 requires DEV-906: feature validation is asserted against dataset fixtures.
- DEV-908 requires DEV-907: single-node correctness before distributed behaviour.
- DEV-909 requires DEV-908: replication presumes a verified distributed cluster.
- DEV-910 requires DEV-908: the baseline measures the distributed deployment.
- DEV-911 requires DEV-906 and DEV-907: comparable means the same tests and data.
- DEV-912 requires DEV-911: differences are only meaningful against a Silo result.
- DEV-913 requires DEV-910 and DEV-911: comparison needs both baselines and parity.
- DEV-914 and DEV-915 require all prior phases; DEV-915 is the only phase that may
  write the recommendation.

DEV-905 is the only authorised phase. No later phase may begin early. Overlap is
permitted only where the dependency is purely documentary and the currently
authorised phase remains the sole active execution scope.

## 6. Deliverables

**Per phase.** A report in `docs/NN-*/README.md` containing all 12 required
sections, a raw-output `evidence/` directory backing every PASS, sanitised
`screenshots/`, and a `DEVIATIONS.md` entry for anything that departed from
requirement. Large artefacts are referenced by digest and stored outside the
repository.

**Across the Epic.** A capability matrix covering every feature and objective; a
performance comparison with variance and an explicit indicative label; a security,
licensing and maintenance review with dated CVE data; the replication runbook; and a
go/no-go recommendation with its conditions and residual risks.

**Governance.** `DEVIATIONS.md`, `OUT_OF_SCOPE.md`, this plan, and the phase
directory structure.

## 7. Gates

A phase gate is passed only when its gate condition is met with evidence, the phase
report is complete, the lab is left in its declared state, and any deviation is
recorded. A gate is never passed on intent, and never passed with a known open defect
that affects the gate condition.

Gate failures are recorded as failures with the evidence that produced them. A phase
that cannot pass its gate in this environment records the blocker and continues with
the phases that do not depend on it, rather than reporting success.

## 8. Evidence

Evidence is the primary record; conclusions are downstream of it.

| Rule | Requirement |
|---|---|
| Capture before concluding | Raw output captured before any result is written |
| Text, not screenshots | Screenshots support, they do not prove |
| Named per test case | `TC-<test-id>-<product>.txt` |
| Failures retained | Never deleted or overwritten (guardrail 19) |
| Ground truth committed | The reference every integrity check compares against is in version control |
| Dated retrieval | Every time-sensitive claim carries its retrieval date |
| Sanitised | No credentials, hostnames, domains, addresses, or customer data |
| Never altered | Captured evidence is not edited after capture; superseded evidence is superseded by a new file with a pointer to the old one |

Destructive operations follow a fixed sequence: record state, identify reclaimable
resources, obtain authorisation, act, re-measure, record the result. The
authorisation and the before/after measurement are both evidence.

## 9. Documentation

One directory per phase, named for the phase, each with `README.md`, `evidence/` and
`screenshots/`. Governance documents live at the repository root. The documentation
pack supplied to the execution agent is agent instruction material and is excluded
from version control.

Documentation is written to be re-readable by someone who was not present: expected
results recorded before observation, reproduction steps that work from a clean
checkout, and explicit statements of what was not tested.

## 10. Risks and blockers

Format per phase: Problem → Decision → Action → Evidence → Current status. Full
history is retained; superseded entries are marked, never deleted.

| ID | Problem | Decision | Action | Evidence | Status |
|---|---|---|---|---|---|
| R1 | Host below Profile A/B reference | Approved deviation, not a new profile | Record required vs actual per phase; label results indicative | D-019 | Closed as approved deviation |
| R2 | 608 MB free disk blocked all phases | Reclamation authorised in three tiers | Preserve ground truth, then reclaim; re-measure each tier | `docs/01` disk evidence | In progress |
| R3 | VMware guest host | Approved deviation | Record in environment section | D-019 | Closed as approved deviation |
| R4 | `mcli` and `fio` absent from host | `mcli` from the pinned product image; `fio` as a pinned container | Extract and record version plus checksum; build and prove the container | `docs/01` tool evidence | In progress |
| R5 | O05/O08 recorded as having no basis | Vendor publishes all eight conditions; capture then test | Capture authoritative text with retrieval date; test each condition against both products | D-022 | Open until captured in DEV-912 |
| R6 | D-012/D-013 stale under the current pack | Supersede with dated entries | Record supersession; DEV-907 becomes genuinely single-node | D-012, D-013 | In progress |
| R7 | Multipart ETag handling produces false mismatches | Fix the comparison logic, prove with a negative control | Confirmed at `verify-manifest:186`, which compares ETag straight to local MD5 and cannot match for any multipart object. Fix the comparison, then prove it with negative controls | `docs/02` tool-provenance-audit.txt | Open |
| R8 | No NFS environment | Build as a pinned container | Build, prove, measure; record Not Available with reason only if it cannot be built | DEV-910 evidence | Open |
| R9 | Tracker and README conflicted with reality | README is reconciled to measured state | Rewrite status from evidence, not from the old tracker | `README.md` | Closed |
| R10 | Public repository; history retains removed docs | Scan working tree **and** history before publishing | Run secret scan across tree and full history | `docs/01` scan evidence | In progress |
| R11 | Documentation did not match the phase structure | Migrate with `git mv`, preserve evidence | Migrate to 11 phase directories; add the replication directory; rewrite references | Migration commit | Closed |
| R12 | NFS in a container may need capabilities unavailable in this guest | Verify early rather than late | Attempt build in DEV-905; record Not Available with reason if it fails | `docs/01` evidence | Open |
| R13 | A reported server-side capture is absent from the repository | Treat the claim as unverified, not as a result | Confirmed absent from the working tree **and** from Git history; `dataset-manifest.jsonl` is also absent. Report corrected with a tabulated audit trail | `docs/02` tool-provenance-audit.txt; manager report corrections | Open |
| R14 | Ground-truth manifest untracked, only in ignored `lab/data/` | Ground truth must be in version control before any deletion | Copy manifest, summary and provenance into evidence and commit | `7e15f50` | **Closed** |
| R15 | Silo ships its own client symlinked as `mc`, inviting an unfair comparison | One client drives both products | Use MinIO's `mc` for both; use `mcli` only where it is the only option; record both versions | Fairness record | Closed |
| R16 | MinIO console default port already in use | Explicit port allocation | Allocate non-default ports and record the map | `docs/01` evidence | Closed |
| R17 | Live lab contradicts the current phase structure | Do not reuse as-is | Rebuild the lab to the phase structure and re-baseline | DEV-905 evidence | Closed |
| R18 | Tool changes committed under an unrelated message | An unaudited code change must not be mistaken for reviewed work | `capture-manifest` and `verify-manifest` were swept into `a8bc2f9` by a broad `git add -A`. Validated (syntax, usage paths) and documented rather than reverted, since the changes are sound | `docs/02` tool-provenance-audit.txt | Closed |

**Residual risk to the conclusion.** Performance results cannot support capacity or
production-sizing conclusions. The dataset is below the Profile B floor. Both are
recorded in every performance and dataset artefact, not only in this table.

## 11. Stop conditions

Work stops and the blocker is recorded when any of these occur:

- A destructive operation is about to run without recorded authorisation.
- A credential, key or secret would be committed.
- MinIO and Silo would occupy the same cluster.
- A result would be recorded without captured evidence.
- The next phase is not authorised.
- Disk space is insufficient to complete the current phase safely.
- A guardrail would have to be broken to proceed.

Stopping is not failure. An unrecorded workaround is failure.

## 12. Epic Definition of Done

1. DEV-905 through DEV-915 each pass their gate with complete reports and evidence.
2. Every required feature has an expected result, an actual result and evidence.
3. Every O01–O08 condition has an evidence-backed applies / does-not-apply decision.
4. Performance comparison uses identical methodology, reports repetitions and
   variance, and is labelled as controlled-environment indicative.
5. Dataset integrity is verified against a committed ground-truth manifest, proven
   by a negative control.
6. Security, licensing, maintenance and CVE review complete with dated sources.
7. Capability matrix and go/no-go recommendation produced from evidenced results.
8. Final QA checklist passes in full.
9. Every deviation recorded with reason, impact and current status.
10. Repository is reproducible by a reader with no access to the original host.

Items 4 and 5 carry a standing qualification: this environment cannot satisfy the
Profile B dataset floor or produce authoritative performance figures. Both are
recorded as such, and the DoD is met by reporting the gap accurately, not by
removing it.

## 13. Final repository structure

```text
.
├── README.md                        # Status, method, limitations
├── DEVIATIONS.md                    # Every departure, with Problem→Decision→Action→Evidence→Status
├── DEV-904-EXECUTION-PLAN.md        # This document
├── OUT_OF_SCOPE.md                  # Explicit exclusions
├── .gitleaks.toml                   # Secret-scanning configuration
├── .pre-commit-config.yaml          # Hooks: secrets, mixed clusters, environment claims
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
│   ├── compose/                     # minio, silo, proxy, workload, monitoring
│   ├── images/                      # Pinned image builds
│   └── data/                        # Cluster data and dataset (not committed)
├── tools/
│   ├── bin/                         # lab, gen-dataset, seed-dataset, capture/verify-manifest, checks
│   └── build-minio.sh               # Reproducible MinIO build
└── scripts/                         # Standalone checks invoked by hooks
```

`DEV-904-project-documentation-pack/` is agent instruction material and is excluded
from version control by `.gitignore`.

---

## Current authorisation

| Item | State |
|---|---|
| DEV-905 | **Authorised** |
| DEV-906 – DEV-915 | Not authorised |
| Disk reclamation, three tiers | Authorised, ground truth preserved first |
| Publishing to the public remote | Authorised, after secret scan passes |

The next phase may not begin until this one passes its gate and is separately
authorised.