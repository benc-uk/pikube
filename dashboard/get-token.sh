#!/bin/bash
#kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')

kubectl -n kubernetes-dashboard get secret -o=jsonpath="{$.items[?(@.metadata.annotations.kubernetes\.io/service-account\.name == 'admin-user')].data.token}{'\n'}" | base64 -d