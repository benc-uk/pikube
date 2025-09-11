# Setup NFS server and Storage class

Main info taken from:
https://medium.com/codex/reliable-kubernetes-on-a-raspberry-pi-cluster-storage-ff2848d331df

First nominate a node as the NFS server and which will store the exported data locally on this host, but share it over the network to any pod/node that needs it

```sh
NFS_NODE=node1

# The exported NFS directory needs to exist first
ssh $NFS_NODE sudo mkdir /nfs
kubectl label node $NFS_NODE nfs=enabled
```

Then we deploy the NFS server, due to the previous label the pod will only be run on node we specified

```sh
kubectl apply -f ./storage/nfs.yaml
```

### Option 1. 

Then run the script which will create the volumes and shares. Pass in the hostname of the same node as used above, and number of volumes to create. E.g.

```sh
./storage/volumes.sh node1 5
```

### Option 2.

- Run this command to get the IP address of the NFS server `kubectl get svc -n storage nfs-server -o jsonpath='{.spec.clusterIP}'`
- SSH into the node you are using for NFS, and create sub-directory inside the `/nfs/` directory, e.g. `mkdir -p /nfs/share_blah`
- Change the name, label, path and server in the YAML before applying

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-nfs-share # Change me
  labels:
    share: "blah" # Change me
spec:
  capacity:
    storage: 500Mi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /share_blah  # Change me, don't include the /nfs/ part
    server: {{NFS_SERVER_IP}}  # Change me
```