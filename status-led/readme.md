# Kubernetes Status Display LED Matrix
Sample code for displaying the status of your cluster in various ways on a external LED board attached to one of the Raspberry Pis

[It kinda looks like this](https://twitter.com/BenCodeGeek/status/1266836870811582465?s=20)

# Hardware
I used this [Allo Rainbow HAT - 8x8 LED Matrix](https://thepihut.com/products/allo-rainbow-hat-8x8-led-matrix)  
I think [this Unicorn HAT](https://shop.pimoroni.com/products/unicorn-hat) is also the same thing 

# Library Install
**⚠ DO NOT TRY TO USE THE ALLOCOM LIBRARY https://github.com/allocom/Rainbow-HAT  
IT DOESN'T WORK. I WASTED HOURS ON IT ⚠**

Use this instead https://github.com/pimoroni/unicorn-hat

Quick setup
```bash
curl -sS https://get.pimoroni.com/unicornhat | bash
```

Also install the [kubernetes client for Python ](https://github.com/kubernetes-client/python)

```bash
pip3 install kubernetes
```

# Display 1 - Pod Status
From whatever node has the LED HAT installed
```bash
sudo python3 ./status-led/pod-status.py
```

# Display 2 - Nodes CPU & Memory
todo