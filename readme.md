# Project PiKube
A slightly grand title for a very quick "brain dump" style guide on building a small set of Raspberry Pis and installing a Kubernetes cluster on them

<img src="https://user-images.githubusercontent.com/14982936/83271709-21bd4180-a1c2-11ea-9849-8690fe02106d.png" style="width:450px">

# Prereqs
## Software
- https://www.balena.io/etcher/
- SSH client
- Decent terminal/shell
- kubectl (optional but reccomended)
  

## Hardware
This is what I used
- 3 x Raspberry Pi 4
- 3 x microSDHC cards (I used 32GB, I'm sure 16GB would work too)
- 3 x [Short 30cm USB C cables](https://www.amazon.co.uk/gp/product/B07W12JK3J/)
- 1 x [Multi port USB Power block](https://www.amazon.co.uk/gp/product/B00VTI8K9K)
- 2 x [Cluster case / rack](https://thepihut.com/products/cluster-case-for-raspberry-pi)

I used 1 RPi as a master node, and 2 as worker nodes

# Source Guides
My notes here all are borrowed/copied/taken from the two guides below. There's nothing new unique on this page which isn't covered by these guides

**Kubernetes on Raspbian (Raspberry Pi)**   
https://github.com/teamserverless/k8s-on-raspbian

**How to build your own Raspberry Pi Kubernetes Cluster** 
https://wiki.learnlinux.tv/index.php/How_to_build_your_own_Raspberry_Pi_Kubernetes_Cluster#.3D.3D_Enable_routing


# 1. Basic OS Setup 

- Flash each SD with 'Raspbian Buster Lite'  
https://www.raspberrypi.org/downloads/raspbian/

- Enable SSH  
Touch empty `ssh` file in boot partition

- Enable WiFi  
https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

- SSH onto each 
  - Get IP of each from your router status / connected devices
  - `ssh pi@{ip_address}` (default password: `raspberry`) 
  - *Optional*: `ssh-copy-id pi@foo` to copy SSH keys
  - *Optional*: `sudo passwd pi` to change password

- Assign hostnames and **static** IPs
  - Hostname: `sudo nano /etc/hostname`
  - edit `sudo nano /etc/dhcpcd.conf` (see etc/dhcpd-snippet.conf)


# 2. Base Config
Setup 
```bash
sudo apt update && sudo apt dist-upgrade
sudo apt install -y git
sudo sysctl net.bridge.bridge-nf-call-iptables=1
```

Disable swap
```bash
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile
```

Edit kernel boot command `/boot/cmdline.txt`  
Add the following to the end
```bash
cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
```

**⚠ IMPORTANT** Enable IP forwarding (pod to pod overlay network will not work otherwise)  
`sudo nano /etc/sysctl.conf`

Uncomment this line
```bash
#net.ipv4.ip_forward=1
```


# 3. Docker
Full setup script here https://github.com/benc-uk/tools-install/blob/master/docker-engine.sh 

It boils down to just this:
```bash
curl -fsSL https://get.docker.com/ | sh
sudo groupadd docker || true
sudo usermod -aG docker $USER
```


# 4. Kubernetes
Install `kubeadm` on **all nodes** 
```bash
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - 
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update -q
sudo apt-get install -qy kubeadm
```

### Build Master Node / Control Plane
This is it, creating a Kubernetes cluster. The `sudo kubeadm init` command might take a few minutes
```bash
sudo kubeadm config images pull -v3
sudo kubeadm init --token-ttl=0 --pod-network-cidr=10.244.0.0/16
```
**⚠ IMPORTANT** Make a note of the join details, this will be shown once the init process is complete

Get config for kubectl
```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
*Optional but recommended*: scp the .kube/config file to outside the master for remote admin from your dev machine or other system

Validate 
```bash
kubectl get version
```

### Worker Nodes

On each node, join them to cluster with `kubeadm` and the token/hash details from the master init step
```
kubeadm join {IP_ADDRESS}:6443 --token {TOKEN}--discovery-token-ca-cert-hash {CA_HASH}
```

Validate 
```bash
kubectl get nodes
```

### Network 

Install Flannel overlay network.  
[Many other options are available](https://kubernetes.io/docs/concepts/cluster-administration/addons/#networking-and-network-policy)
```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

Validate and check the coredns pods start up
```bash
kubectl get po -n kube-system -l k8s-app=kube-dns
```

### Test with Demo App
Deploy a test Node.js web app, this will create a NodePort service on port 30001
```bash
kubectl apply -f manifests/testapp.yaml
```

Check you see the three pods start, go to `http://{IP_OF_A_NODE}:30001`  
Optionally validate you can ping from pod to pod by exec'ing into them, especially check pod-to-pod across nodes.


# 5. Optional Cluster Tasks

### Deploy NGINX Ingress Controller
```bash
./ingress/deploy.sh
```
This uses a NodePort service on port 30000 and installs using Helm 3 into kube-system namespace

### Deploy & Access Dashboard
```bash
./dashboard/deploy.sh
kubectl apply -f ./dashboard/account.yaml
./dashboard/get-token.sh
```
Copy the token that is output

Then run
```bash
kube proxy
```

Access dashboard here [`http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/`](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/) and login with the token

# Todo
- Use MetalLB for LoadBalancer? https://metallb.universe.tf/
- DNS?
- Certmanager?
- Run blockchain (joke)