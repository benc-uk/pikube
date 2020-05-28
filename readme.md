# Prereq: Software
- https://www.balena.io/etcher/
  
# Prereq: Hardware
- 3 x Raspberry Pi 4
  - SD cards (I used 32GB, I'm sure 16GB would work too)
  - USB C cables
- Multi port USB Power block

# Main Guide
Basically just follow this - **Kubernetes on Raspbian (Raspberry Pi)**   
https://github.com/teamserverless/k8s-on-raspbian


# 1. Basic OS Setup 

- Flash each SD with 'Raspbian Buster Lite'  
https://www.raspberrypi.org/downloads/raspbian/

- Enable SSH  
Touch empty `ssh` file in boot partition

- Enable WiFi  
https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

- SSH onto each 
  - Get IP of each from your router status / connected devices
  - ssh `pi@{ip_address}` 
    - Passwd: `raspberry`
  - *Optional*: `ssh-copy-id pi@foo` to copy SSH keys
  - *Optional*: `sudo passwd pi` to change password

- Assign hostnames and **static** IPs
  - Hostname: `sudo nano /etc/hostname`
  - edit `sudo nano /etc/dhcpcd.conf` (see etc/dhcpd-snippet.conf)

# 2. Base Config

```
sudo apt update && sudo apt dist-upgrade
sudo apt install -y git
sudo sysctl net.bridge.bridge-nf-call-iptables=1
```

Disable swap
```
sudo dphys-swapfile swapoff && \
sudo dphys-swapfile uninstall && \
sudo systemctl disable dphys-swapfile
```

Edit kernel boot command `/boot/cmdline.txt`  
Add the following to the end
```
cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
```

### OPTIONAL: Personal Dotfiles & Zsh
*Very optional*
```
git clone https://github.com/benc-uk/dotfiles .dotfiles
sudo apt install -y zsh
chsh -s /usr/bin/zsh $USER
~/.dotfiles/install.sh
```

# 3. Docker
Full setup script here https://github.com/benc-uk/tools-install/blob/master/docker-engine.sh  
```
curl -fsSL https://get.docker.com/ | sh
sudo groupadd docker || true
sudo usermod -aG docker $USER
```

# 4. Kubernetes
Install kubeadm
```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - 
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update -q
sudo apt-get install -qy kubeadm
```

# Other Stuff / Appendix

Rainbow LED thing  
https://github.com/pimoroni/rainbow-hat

LoadBalancer
https://metallb.universe.tf/

