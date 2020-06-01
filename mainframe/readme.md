# IBM Mainframe Emulation
Running an IBM S/370 mainframe running MVS 3.8  
Running in Docker container  
In a Kubernetes Pod  
On a Raspberry Pi

Why?

Because you can...

### The MVS 3.8j Tur(n)key 4- System
http://wotho.ethz.ch/tk4-/

### tk4 Docker Image
https://github.com/RattyDAVE/docker-ubuntu-hercules-mvs

Slightly modified version of this image that starts correctly on ARM is available here:

```bash
bencuk/hercules-mvs:latest
```
[Dockerfile for this image is in this folder](./Dockerfile)