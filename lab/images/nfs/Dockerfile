# NFS server — provides the NFS-backed storage case for DEV-910.
#
# WHY THIS EXISTS
# ---------------
# The MinIO performance baseline is specified as local versus NFS-backed storage.
# No NFS environment exists on this host. D-010 decided to containerise both `fio`
# and NFS so both products could be measured the same way; D-018 recorded that
# neither had actually been built. This image is the NFS half of that work.
#
# NFS SERVER REQUIREMENTS (recorded because they are easy to get wrong)
# -------------------------------------------------------------------
# An NFS *server* is kernel-backed: rpc.nfsd needs the host `nfsd` module and the
# nfsd filesystem. A client-side mount needs no such thing. This distinction is
# why an NFS "image" alone is not sufficient.
#
# Verified on this host before this image was written:
#   - `nfsd` was NOT in /proc/filesystems
#   - the module exists for the running kernel at
#     /lib/modules/7.0.0-34-generic/kernel/fs/nfsd/nfsd.ko.zst
#   - `nfsd` loaded successfully from a privileged container and is now present
#     in the host's /proc/filesystems
#
# CONSEQUENCE FOR THE OPERATOR. Loading `nfsd` mutates the host kernel and
# persists until it is unloaded. It was loaded to make this environment
# possible. Unload with `modprobe -r nfsd` if the host must return to its
# original module set.
#
# The container therefore needs --privileged and /lib/modules mounted. This is a
# deliberate, recorded exception to the project's usual least-privilege posture,
# and it is scoped to this one service. It grants no additional privilege to
# either object-storage product, which continue to run unprivileged.

FROM alpine@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6

RUN apk add --no-cache nfs-utils=2.6.4-r6 rpcbind=1.2.9-r0

# Storage handed to the products. Bind-mounted by the caller.
VOLUME /export

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# The script mounts the nfsd filesystem, exports, starts rpcbind and then
# rpc.nfsd, because each step depends on the previous one. See entrypoint.sh.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["--nfs-version", "4"]