#!/bin/bash

while read line; do

  KEY=$(echo $line| awk -F'=' '{print $1}')

  VALUE=$(echo $line| awk -F'=' '{print $2}')

  echo -n $KEY=

  etcdctl set $KEY "$VALUE"

done < "${1:-/dev/stdin}"