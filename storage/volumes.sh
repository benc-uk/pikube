#!/bin/bash

#
# This hacky script creates NFS shared dirs and PersistentVolume objects
# You're probably going to want to edit this to match your environment
#

NFS_HOST=$1
SHARE_COUNT=$2

if [ -z "$NFS_HOST" ] || [ -z "$SHARE_COUNT" ]; then
  echo "Usage: $0 <nfs-host> <share-count>"
  exit 1
fi

NFS_SERVER_IP=$(kubectl get svc -n storage nfs-server -o jsonpath='{.spec.clusterIP}')

# Name of the host/worker where the NFS server pod is running
NFS_HOST=node1

for i in $(seq 1 "$SHARE_COUNT"); do
  i=$(printf "%02d" "$i")

  # Assumes SSH key access without password to the NFS server, your setup may vary
  ssh "$NFS_HOST" "sudo mkdir -p /nfs/share_$i"

  kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-share-$i
  labels:
    share: "$i"
spec:
  capacity:
    storage: 500Mi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /share_$i
    server: $NFS_SERVER_IP
EOF

done
