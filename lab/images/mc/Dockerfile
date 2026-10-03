# mc client image.
#
# WHY THIS EXISTS
# ---------------
# `minio/mc` was deleted from Docker Hub (HTTP 404) and the historical binary
# host dl.min.io now returns HTTP 410 Gone. The only remaining official
# distribution channel is the GitHub release asset for the last release,
# RELEASE.2025-08-13T08-35-41Z, which this image is built from.
#
# The staged ./mc binary is the official asset and its sha256 was verified
# against the upstream .sha256sum file before staging:
#   01f866e9c5f9b87c2b09116fa5d7c06695b106242d829a8bb32990c00312e891
# Verification evidence: docs/01-repo-versions-and-lab/evidence/
#
# Base matches the MinIO baseline image so the client is not a hidden variable
# between the MinIO and Silo test runs, so the client is never the reason for a
# difference between the products.

FROM registry.access.redhat.com/ubi9/ubi-micro@sha256:932aec77f5b86a5dba854a18b14a38725b296967e7dc9c7a1f4d7f0bf82e1ce5

COPY mc /usr/bin/mc

# Config dir must be writable by an arbitrary UID; matches Silo's image, which
# also sets MC_CONFIG_DIR under /tmp.
ENV MC_CONFIG_DIR=/tmp/.mc \
    HOME=/tmp

ENTRYPOINT ["/usr/bin/mc"]
CMD ["--version"]