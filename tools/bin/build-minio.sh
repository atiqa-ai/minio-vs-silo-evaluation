#!/usr/bin/env bash
# Build the MinIO CE baseline image from the archived source tree.
#
# Reproducible from the repository: clones/pins MinIO at the last open-source
# release tag, builds the static binary with upstream's own LDFLAGS mechanism,
# stages it into the image build context, and records the full provenance chain.
#
# Usage: tools/bin/build-minio.sh [--fresh]
#   --fresh  re-clone the source tree from scratch
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOOLS="$REPO_ROOT/tools"
SRC="$TOOLS/src/minio"
GOPATH="$TOOLS/gopath"
GOROOT="$TOOLS/go"
CTX="$REPO_ROOT/lab/images/minio"
OUTDIR="$REPO_ROOT/docs/01-repo-versions-and-lab/evidence"

# The last open-source MinIO Community Edition release. Immutable.
TAG="RELEASE.2025-10-15T17-29-55Z"
TAG_COMMIT="9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a"
# gen-ldflags.go parses this RFC3339-ish form and reassembles the release tag.
TAG_VERSION="2025-10-15T17-29-55Z"
IMAGE_LOCAL="minio-ce-local:RELEASE.2025-10-15T17-29-55Z"

log(){ printf '[%s] %s\n' "$(date +%T)" "$*"; }
die(){ printf 'error: %s\n' "$*" >&2; exit 1; }

mkdir -p "$OUTDIR"

# ---------------------------------------------------------------- toolchain
if [ ! -x "$GOROOT/bin/go" ]; then
  die "Go toolchain missing at $GOROOT. See docs/01-repo-versions-and-lab/README.md step 1."
fi
export PATH="$GOROOT/bin:$PATH" GOPATH GOPROXY=https://proxy.golang.org,direct

# ------------------------------------------------------------------- source
if [ "${1:-}" = "--fresh" ]; then
  log "--fresh: removing existing source tree"
  rm -rf "$SRC"
fi
if [ ! -d "$SRC/.git" ]; then
  log "cloning MinIO (full clone: git describe needs the tag history)"
  git clone --quiet https://github.com/minio/minio.git "$SRC"
fi
cd "$SRC"
git checkout --quiet "$TAG"

GOT_COMMIT="$(git rev-parse HEAD)"
GOT_TAG="$(git describe --tags --abbrev=0)"
[ "$GOT_COMMIT" = "$TAG_COMMIT" ] || die "commit drift: expected $TAG_COMMIT, got $GOT_COMMIT"
[ "$GOT_TAG" = "$TAG" ] || die "tag drift: expected $TAG, got $GOT_TAG"
log "source pinned: $GOT_TAG @ $GOT_COMMIT"

# -------------------------------------------------------------------- build
if [ ! -x "$SRC/minio" ] || [ "${1:-}" = "--fresh" ]; then
  log "generating LDFLAGS via upstream buildscripts/gen-ldflags.go"
  LDFLAGS="$(MINIO_RELEASE=RELEASE go run buildscripts/gen-ldflags.go "$TAG_VERSION")"
  log "building (first run downloads ~700MB of modules; may need retries on flaky links)"
  export CGO_ENABLED=0 GOOS=linux GOARCH=amd64
  for attempt in 1 2 3 4; do
    if go build -tags kqueue -trimpath --ldflags "$LDFLAGS" -o "$SRC/minio"; then
      log "build succeeded on attempt $attempt"; break
    fi
    log "attempt $attempt failed (usually transient proxy errors); retrying"
    [ "$attempt" -lt 4 ] || die "build failed after 4 attempts"
    sleep 5
  done
fi

VERSION_LINE="$("$SRC/minio" --version 2>&1 | head -1)"
case "$VERSION_LINE" in
  *"RELEASE.2025-10-15T17-29-55Z"*) log "version check OK: $VERSION_LINE" ;;
  *) die "binary does not report the expected release tag: $VERSION_LINE" ;;
esac

# ------------------------------------------------------- stage build context
log "staging build context"
cp "$SRC/minio"            "$CTX/minio"
cp "$SRC/dockerscripts/docker-entrypoint.sh" "$CTX/docker-entrypoint.sh"
chmod +x "$CTX/docker-entrypoint.sh"

BIN_SHA="$(sha256sum "$SRC/minio" | cut -d' ' -f1)"

# -------------------------------------------------------------- build image
log "building image $IMAGE_LOCAL"
docker build -t "$IMAGE_LOCAL" "$CTX"

IMG_SHA="$(docker inspect "$IMAGE_LOCAL" --format '{{index .RepoDigests 0}}' 2>/dev/null || true)"
[ -n "$IMG_SHA" ] || IMG_SHA="local-build (no repo digest until pushed)"

# ------------------------------------------------------------- provenance
PROV="$OUTDIR/minio-build-provenance.txt"
{
  echo "MinIO CE baseline image — provenance chain"
  echo "recorded: $(date -Is)"
  echo "reason:   no upstream MinIO CE image is obtainable (Docker Hub 404, quay 401)"
  echo
  echo "upstream_repository   https://github.com/minio/minio"
  echo "upstream_release_tag  $TAG"
  echo "upstream_commit       $GOT_COMMIT"
  echo "go_toolchain          $(go version)"
  echo "build_flags           CGO_ENABLED=0 GOOS=linux GOARCH=amd64 -tags kqueue -trimpath"
  echo "ldflags_generator     buildscripts/gen-ldflags.go (upstream mechanism, MINIO_RELEASE=RELEASE)"
  echo "binary_sha256         $BIN_SHA"
  echo "binary_size_bytes     $(stat -c%s "$SRC/minio")"
  echo "binary_version_line   $VERSION_LINE"
  echo "base_image            registry.access.redhat.com/ubi9/ubi-micro@sha256:932aec77f5b86a5dba854a18b14a38725b296967e7dc9c7a1f4d7f0bf82e1ce5"
  echo "base_image_reason     same base as the Silo image, so neither product gets a different base"
  echo "entrypoint_source     dockerscripts/docker-entrypoint.sh (verbatim from the RELEASE tree)"
  echo "local_image_tag       $IMAGE_LOCAL"
  echo "local_image_id        $(docker inspect "$IMAGE_LOCAL" --format '{{.Id}}')"
  echo "local_image_digest    $IMG_SHA"
} > "$PROV"

log "provenance written to $PROV"
log "image: $IMAGE_LOCAL"
log "done"