# fio — storage-layer benchmark tool for DEV-910.
#
# WHY THIS EXISTS
# ---------------
# The requirements specify `fio` measurements of the storage layer beneath each
# product. `fio` is absent from this host, and D-010/D-018 already withdrew an
# earlier claim that containerised `fio` and NFS tooling had been built. Nothing
# was built; this image is that work.
#
# WHY A CONTAINER
# ---------------
# Both products must be measured with the same tool, and the
# host must stay reproducible from the repository. Installing `fio` onto the host
# would make the measurement depend on host state that a reader cannot reproduce.
# A pinned image makes the tool version part of the recorded evidence.
#
# VERSION PINNING
# ---------------
# The base image is pinned by digest and the package by exact version, not by
# range. `apk add fio=3.41-r0` will fail rather than silently resolve to a newer
# release, so a future rebuild either reproduces this exact tool or fails loudly.
# The resolved version is recorded in
# docs/01-repo-versions-and-lab/evidence/ rather than trusted from this comment.

FROM alpine@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6

RUN apk add --no-cache fio=3.41-r0

# Job files are mounted in by the caller, so the same image serves every
# storage-layer profile and the profile text stays in version control as
# evidence rather than baked into a layer.
WORKDIR /jobs

ENTRYPOINT ["fio"]
CMD ["--version"]