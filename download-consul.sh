#!/bin/sh

mkdir -p playbooks/roles/consul/files/bin

mkdir -p playbooks/roles/etcd2consul/files/bin

wget -c https://releases.hashicorp.com/consul/0.8.5/consul_0.8.5_linux_amd64.zip -O playbooks/roles/consul/files/bin/consul_0.8.5_linux_amd64.zip

wget -c https://github.com/laincloud/etcd2consul/releases/download/v0.0.1/etcd2consul.xz -O playbooks/roles/etcd2consul/files/bin/etcd2consul.xz

unzip -o playbooks/roles/consul/files/bin/consul_0.8.5_linux_amd64.zip -d playbooks/roles/consul/files/bin

unxz -kf playbooks/roles/etcd2consul/files/bin/etcd2consul.xz
