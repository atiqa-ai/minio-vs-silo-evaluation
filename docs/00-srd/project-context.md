# Project Context

## Project

**Evaluate the Last Open-Source MinIO and Silo, Feature by Feature**

---

## Background

Upstream MinIO Community Edition is archived/read-only since **2026-04-25** and receives no further releases or security patches.

Silo is a community-maintained MinIO fork by the Pigsty project.

Silo is intended as a near drop-in replacement.

---

## Silo Compatibility Surface

The project context includes:

* Same S3 surface
* `mc`-style tooling
* Silo's `mcli`
* `MINIO_*` environment variables
* `minio_*` Prometheus metrics
* Same `.minio.sys` on-disk format

Silo additions include:

* Full Console
* `silo healthcheck`
* `mcli checksum verify`
* Distroless image variant

---

## Compatibility Reality

Silo describes compatibility as conditional.

There are eight conditions:

```text
O01–O08
```

Compatibility must be demonstrated test by test.

MinIO and Silo cannot be mixed in one distributed cluster.

---

## Project Model

```text
MinIO
  ↓
Baseline
  ↓
Evidence
  ↓
Silo
  ↓
Same tests
  ↓
Evidence
  ↓
Comparison
  ↓
Capability Matrix
  ↓
Final Evaluation
```

---

## Execution Environment

The project runs on one local workstation/laptop.

Use:

* Docker Engine/Docker Desktop
* Docker Compose v2
* Local SSD
* Synthetic data

No cloud or additional physical infrastructure.

---

## Reference Profile A

```text
8+ CPU
32 GB RAM
200 GB free SSD
4 nodes × 2 drives
Load-balancer container
20–30 GB dataset
```

---

## Reference Profile B

```text
8 CPU
16 GB RAM
100 GB free SSD
4 nodes × 1 drive
Load-balancer container
5–10 GB dataset
```

Reduced benchmark profiles are indicative only.

---

## Required Testing Tools

The project specifically uses:

```text
mc
mcli
warp
fio
Manifest toolkit
```

---

## Required Evidence

Important evidence includes:

* Raw command output
* Screenshots where useful
* Compose files
* `.env.example`
* `docker compose ps`
* Image digests
* Relevant logs
* `mc admin info`
* Heal status
* Replication status/backlog
* Benchmark commands
* Raw benchmark results
* Repeated benchmark runs

---

## Repository Model

```text
minio-vs-silo-evaluation/
```

Each subtask:

```text
docs/NN-name/
├── README.md
├── screenshots/
└── evidence/
```

---

## Project Completion Model

The project moves through:

```text
ST01
Repository + Lab
      ↓
ST02
Test Data + Verification
      ↓
ST03
MinIO Features
      ↓
ST04
MinIO Performance
      ↓
ST05
MinIO Distributed Mode
      ↓
ST06
Silo Functional Validation
      ↓
ST07
S3 + Client Compatibility
      ↓
ST08
Silo Benchmark
      ↓
ST09
Security + License + Maintenance
      ↓
ST10
Capability Matrix + Final Evaluation
```
