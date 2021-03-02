# Notes

Info taken from:

https://medium.com/codex/reliable-kubernetes-on-a-raspberry-pi-cluster-storage-ff2848d331df

- SSH into node-1
  - `sudo mkdir /nfs-vol && exit`
- `kubectl label node node-1 nfs=enabled`
- `kubectl apply -f nfs.yaml`