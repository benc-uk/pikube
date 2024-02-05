# Ingress Controller

This deploys the trusty old NGINX Ingress Controller into the kube-system namespace

```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

Deploy with Helm

```sh
helm install ingress ingress-nginx/ingress-nginx \
  -n kube-system \
  --set controller.service.type=NodePort \
  --set controller.service.nodePorts.http=31000
```