#!/bin/sh
# NFS server entrypoint.
#
# WHY THIS SCRIPT EXISTS
# ----------------------
# An NFS server is kernel-backed, so a container image alone is not enough. The
# nfsd filesystem must be mounted before rpc.nfsd can talk to the kernel.
#
#   mount -t nfsd nfsd /proc/fs/nfsd
#
# Without it, rpc.nfsd fails with "writing fd to kernel failed: errno 111
# (Connection refused)". That error names the kernel rather than the missing
# mount, which is why it is easy to misdiagnose. It was the first failure
# observed on this host.
#
# WHY rpcbind IS NOT RUN
# ----------------------
# An earlier version of this script started `rpcbind -w`. That deadlocked the
# host. Observed stack from a wedged container:
#
#   rpcb_v4_register -> rpc_call_sync -> rpc_wait_bit_killable -> poll
#
# rpcbind was blocked in a synchronous RPC call to unregister its own service,
# waiting on a portmapper reply inside the container's network namespace that
# could never arrive. The syscall was `poll` with a 30 second timeout, retried
# indefinitely, so the process sat in uninterruptible disk-sleep and neither
# `docker stop` nor SIGKILL could clear it. It pinned the nfs and nfsd modules.
#
# NFSv4 does not need rpcbind: v4 registers with the server on port 2049
# directly, and v2/v3 are the versions that depend on the portmapper. Serving
# v4 only removes rpcbind from the picture entirely, and with it the deadlock.
# `rpc.nfsd -N 3` disables the version that would need it.
#
# This is recorded as an open defect rather than a silent fix: the wedged
# container from the earlier attempt could not be cleared without a host reboot.

set -e

echo "nfs-server: mounting nfsd filesystem"
mount -t nfsd nfsd /proc/fs/nfsd

echo "nfs-server: re-reading /etc/exports"
exportfs -r
exportfs -v

# -N 3 disables v3, the version that would need the portmapper. -N 2 is not
# used: this kernel has already dropped NFSv2, and passing it makes rpc.nfsd
# exit with "2: Unsupported version". Verified on this host:
#   -N 3 --nfs-version 4  -> starts
#   --nfs-version 4 alone -> "writing fd to kernel failed: errno 111"
echo "nfs-server: starting rpc.nfsd (NFSv4 only, no rpcbind)"
rpc.nfsd -N 3 "$@"

echo "nfs-server: registered services"
# `rpcinfo` needs a local portmapper, which this container deliberately does not
# run, so it cannot be used to confirm readiness. Report the kernel-side view
# instead, which is the thing that actually matters.
echo "nfs-server: nfsd file handles and versions in /proc/fs/nfsd:"
ls /proc/fs/nfsd 2>&1 | sed 's/^/  /'

echo "nfs-server: ready, idling"
# rpc.nfsd daemonises, so without this the script would exit and stop the
# container, killing the export.
while true; do
    sleep 3600
done