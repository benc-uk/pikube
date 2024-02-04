# Setup NFS server and storage class

Info taken from:

https://medium.com/codex/reliable-kubernetes-on-a-raspberry-pi-cluster-storage-ff2848d331df

Create a directory on one of the nodes to be exported by the NFS server and as many shared directories as you want

SSH into a worker node, e.g. node1 and run
  
```sh
sudo mkdir -p /nfs-vol/share01
sudo mkdir -p /nfs-vol/share02
sudo mkdir -p /nfs-vol/share03
sudo mkdir -p /nfs-vol/share04
sudo mkdir -p /nfs-vol/share05
```

Then deploy the NFS server

- `kubectl label node node1 nfs=enabled`
- `kubectl apply -f nfs.yaml`
