# Evidence — DEV-909

Raw command output for every PASS/FAIL in DEV-909 goes in this directory.

One file per test case, named `TC-<test-id>-<product>.txt`, plus any supporting
captures. Evidence is plain text: raw command output, not a retyped summary
(evidence guide, section 5). Failures are kept, never deleted (guardrail 19).

Replication is MinIO-to-MinIO, so `<product>` is `minio` on both sides; the
source and target are distinguished in the file body and in the filename.
