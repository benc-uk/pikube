# Monitoring with Grafana & Prometheus

This short guide will deploy Grafana & Prometheus to the cluster.

We will need to use [Helm](https://helm.sh/) for this. If you don't have it installed you can run `https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash` to quickly install the helm binary.

First add the chart repos

```sh
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

Before running the next part set up storage see [the instructions here](./storage-nfs.md)
_Optional:_ If you are OK with not having persistence for Grafana, simply remove the persistence part in the YAML below

```sh
helm install grafana grafana/grafana -f ./samples/values/grafana.yaml
```

Deploy kube-state-metrics (KSM) so we get more stats and metrics from our cluster

```sh
helm install state-metrics prometheus-community/kube-state-metrics --set prometheus.monitor.enabled=true --set prometheus.scrapeconfig.enabled=true
```

Now deploy Prometheus

```sh
helm install prometheus prometheus-community/prometheus -f ./samples/values/prometheus.yaml
```

Now access Grafana from the exposed NodePort on any of the nodes, the port will be 32200, e.g. http://192.168.0.150:32200/

When adding Prometheus data source to Grafana, you should use the following URL `http://prometheus-server` (which is the internal service name)

To see some of the data being collected, in Grafana try importing Dashboard with ID `11074` this will give you a 'Node Exporter' dashboard with many pretty charts and numbers to look at
