# MinIO Community Edition — baseline image, reconstructed from source.
#
# WHY THIS EXISTS
# ---------------
# `minio/minio` was deleted from Docker Hub (HTTP 404) and `quay.io/minio/minio`
# now rejects anonymous pulls (HTTP 401). No upstream MinIO CE container image
# is obtainable. MinIO's own Dockerfile at RELEASE.2025-10-15T17-29-55Z is a thin
# wrapper (`FROM minio/minio:latest`) that only copies a prebuilt binary, so it
# cannot be used either.
#
# This image is therefore built from the archived source tree at the last
# open-source release tag. See docs/01-repository-and-lab/evidence/ for the
# recorded provenance chain (git tag, commit, Go toolchain, binary sha256,
# image digest).
#
# BASE IMAGE CHOICE
# -----------------
# ubi9-micro is the same base Silo's image uses, so that the MinIO and Silo
# containers differ only in the object-storage implementation under test. This
# is required by the Identical-Test Rule (guardrails 6) for ST08 performance
# comparison to be fair.
#
# Pinned by digest, not tag: the base is a third-party image and the SRD 4.3
# immutability rule applies to it as well.

FROM registry.access.redhat.com/ubi9/ubi-micro@sha256:932aec77f5b86a5dba854a18b14a38725b296967e7dc9c7a1f4d7f0bf82e1ce5

# Upstream MinIO entrypoint, copied verbatim from the RELEASE tree.
# NOT replaced by Silo's: Silo's entrypoint rewrites argv and adds a writable
# HOME shim, which would change MinIO's own behaviour and invalidate the
# baseline.
COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh

# Statically linked binary (CGO_ENABLED=0), built by tools/bin/build-minio.sh
COPY minio /usr/bin/minio

# Parity with the Silo image: same MINIO_* file-based credential variables,
# same HOME override. Silo still honours MINIO_* names, so the baseline must
# expose the identical surface for ST07 configuration-compatibility testing.
ENV MINIO_ACCESS_KEY_FILE=access_key \
    MINIO_SECRET_KEY_FILE=secret_key \
    MINIO_ROOT_USER_FILE=access_key \
    MINIO_ROOT_PASSWORD_FILE=secret_key \
    MINIO_KMS_SECRET_KEY_FILE=kms_master_key \
    MINIO_CONFIG_ENV_FILE=config.env \
    HOME=/tmp

VOLUME /data

# Same port Silo exposes. Console port is not exposed in this image; ST09
# reviews console availability separately.
EXPOSE 9000

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]
CMD ["minio"]