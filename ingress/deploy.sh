#!/bin/bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress ingress-nginx/ingress-nginx \
-n kube-system \
--set controller.service.type=NodePort \
--set controller.service.nodePorts.http=30000 \
--set controller.image.repository=quay.io/kubernetes-ingress-controller/nginx-ingress-controller-arm \
--set controller.image.tag=0.32.0