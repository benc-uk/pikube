# Ingress Controller

This deploys the trusty old NGINX Ingress Controller into the kube-system namespace

```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```

Deploy with Helm

```sh
helm install ingress ingress-nginx/ingress-nginx \
  --namespace ingress --create-namespace \
  --set controller.service.type=NodePort \
  --set controller.service.nodePorts.http=31000
```

Your ingress controller should now be running

```sh
kubectl get pods -n ingress
```

You can access it on any node IP on port 31000

```sh
curl http://<node-ip>:31000
```

Until you deploy some ingress resources you'll get a 404 or 503 error, but at least you know it's working
