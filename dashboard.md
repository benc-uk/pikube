# Deploy the Kubernetes Dashboard

Deploy the official Kubernetes Dashboard, which is terrible and no-one ever uses it

It's recommended to deploy the metrics server too `kubectl apply -f samples/metrics-server.yaml`

See also:
- https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/
- https://github.com/kubernetes/dashboard

## 1. Deploy dashboard resources 

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

## 2. Create account

Create a service account called `admin-user` with cluster-admin role

```sh
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard

---

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF
```

## 3. Get an bearer token for that account

```sh
kubectl -n kubernetes-dashboard create token admin-user
```

## 4. Access the dashboard via the API proxy

```sh
kubectl proxy
```

Go to this URL and use the token you created to login

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login