# Storage using NFS and dynamic provisioning

This is a mini guide to setting up NFS based storage for your cluster, so you can use persistent volumes in your pods.
This approach differs from the one in the main [storage](./storage/) guide as it uses dynamic provisioning of volumes, so you don't need to create each volume manually.

## Prepare the disk

Assume you have a USB disk attached to your Pi, e.g. `/dev/sda`

- `sudo fdisk /dev/sda`
  - Delete existing partition(s), create a single partition that uses the whole disk, write and exit
- `sudo mkfs -t ext4 /dev/sda1`

You can skip this entirely and just use an existing directory on your Pi if you prefer.

## Set up NFS server

On the node you want to use as the NFS server, install & configure the NFS server
Follow this guide https://opensource.com/article/20/5/nfs-raspberry-pi

When exporting the NFS share, I used

```
/srv/nfs    *(rw,sync,no_root_squash,no_all_squash,no_subtree_check)
```

I tried the IP based approach but it didn't work for me, so I just allowed all clients.

## Install the NFS dynamic provisioner

We'll use the [NFS subdir external provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner) which will create sub-directories in the NFS share for each persistent volume claim (PVC) that is created.

Note I used node2 as the NFS server, change this to whatever your NFS server node is called.

```sh
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install --namespace kube-system nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=node2 \
    --set nfs.path=/srv/nfs
```

Test it out by creating a test claim and pod, best do this in the `default` namespace

```
kubectl create -f https://raw.githubusercontent.com/kubernetes-sigs/nfs-subdir-external-provisioner/master/deploy/test-claim.yaml -f https://raw.githubusercontent.com/kubernetes-sigs/nfs-subdir-external-provisioner/master/deploy/test-pod.yaml
persistentvolumeclaim/test-claim created
```
