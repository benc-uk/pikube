# IBM Mainframe Emulation

## 🔥🔥🔥 CURRENTLY BROKEN (Feb 2024)

Running an IBM S/370 mainframe running MVS 3.8  
Running in Docker container  
In a Kubernetes Pod  
On a Raspberry Pi

Why?

Because you can...

### The MVS 3.8j Tur(n)key 4- System

- http://wotho.ethz.ch/tk4-/ (link is dead now)
- [This blog](https://bradricorigg.medium.com/run-your-own-mainframe-using-hercules-mainframe-emulator-and-mvs-3-8j-tk4-55fa7c982553) has some more info

### tk4 Docker Image

https://github.com/RattyDAVE/docker-ubuntu-hercules-mvs

However this will not run on a Raspberry Pi, so modified version of this image that starts correctly on ARM is available here:

```bash
bencuk/hercules-mvs:latest
```

[Dockerfile for this image is in this folder](./Dockerfile)