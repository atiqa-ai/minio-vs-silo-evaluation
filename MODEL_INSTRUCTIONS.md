# Instructions for the AI Model Completing This Project

You are executing the **MinIO vs Silo Evaluation** project.

## Mandatory Reading Order

1. `docs/00-srd/README.md`                  ← Project requirements (highest priority)
2. `docs/00-guardrails/README.md`           ← Strict rules you must never violate
3. `docs/00-evidence-guide/README.md`       ← How to record evidence
4. `docs/00-test-cases/README.md`           ← All test cases
5. `docs/00-subtask-tracker/README.md`      ← Completion criteria for each ST

## Execution Order

Execute subtasks strictly in order:

```text
ST01 → ST02 → ST03 → ST04 → ST05 → ST06 → ST07 → ST08 → ST09 → ST10
```

Do not skip any subtask.

## Critical Rules (Never Break)

- MinIO is always the baseline. Test MinIO first, then Silo.
- Never mix MinIO and Silo nodes in the same cluster.
- Use only immutable `RELEASE.*` image tags. Record digests.
- Use only synthetic data.
- Every PASS/FAIL needs raw command output saved in the corresponding `evidence/` folder.
- Failures must remain failures. Do not hide or rewrite them.
- Do not expand scope. Do not introduce Kubernetes, cloud, Terraform, etc.
- Final recommendation must be one of: `Go` | `No-Go` | `Go-with-Conditions`.

## How to Work on Each Subtask

1. Read the corresponding `docs/NN-*/README.md` placeholder.
2. Update the Status to `In Progress`.
3. Write the full README following the 12 required sections.
4. Save all raw evidence in `evidence/`.
5. Add screenshots only if useful (and sanitize them).
6. When everything is done and evidence is present, set Status to `Complete`.
7. Update the status table in the root `README.md`.

## Starting Point

Begin with **ST01 — Repository and Lab**.

Create the Docker Compose lab, pin the last MinIO Community Edition `RELEASE.*` tag and the current Silo `RELEASE.*` tag, record digests, create `migration-net`, and verify the basic environment.

Good luck. Stay inside the SRD and Guardrails at all times.
