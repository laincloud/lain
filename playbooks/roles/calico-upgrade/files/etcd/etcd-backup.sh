#!/bin/bash

KEYS=$(etcdctl ls --recursive -p /docker/network/v1.0/network/)
KEYS+=$(etcdctl ls --recursive -p /calico)

for KEY in $KEYS; do

  # Skip etcd directories

  if [ "${KEY: -1}" == "/" ]; then continue; fi
  echo $KEY=$(etcdctl get $KEY)

done