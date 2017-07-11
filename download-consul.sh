#!/bin/sh

mkdir -p playbooks/roles/consul/files

mkdir -p playbooks/roles/prometheus/files/bin

wget -c https://releases.hashicorp.com/consul/0.8.5/consul_0.8.5_linux_amd64.zip -O playbooks/roles/consul/files/bin/consul_0.8.5_linux_amd64.zip

unzip -o playbooks/roles/consul/files/bin/consul_0.8.5_linux_amd64.zip -d playbooks/roles/consul/files/bin

wget -c https://github.com/prometheus/prometheus/releases/download/v1.7.1/prometheus-1.7.1.linux-amd64.tar.gz -O playbooks/roles/prometheus/files/bin/prometheus-1.7.1.linux-amd64.tar.gz

tar -xzf playbooks/roles/prometheus/files/bin/prometheus-1.7.1.linux-amd64.tar.gz -C playbooks/roles/prometheus/files/bin/

wget -c https://github.com/prometheus/node_exporter/releases/download/v0.14.0/node_exporter-0.14.0.linux-amd64.tar.gz -O playbooks/roles/prometheus/files/bin/node_exporter-0.14.0.linux-amd64.tar.gz

tar -xzf playbooks/roles/prometheus/files/bin/node_exporter-0.14.0.linux-amd64.tar.gz -C playbooks/roles/prometheus/files/bin/

wget -c https://github.com/prometheus/statsd_exporter/releases/download/v0.4.0/statsd_exporter-0.4.0.linux-amd64.tar.gz -O playbooks/roles/prometheus/files/bin/statsd_exporter-0.4.0.linux-amd64.tar.gz

tar -xzf playbooks/roles/prometheus/files/bin/statsd_exporter-0.4.0.linux-amd64.tar.gz -C playbooks/roles/prometheus/files/bin/

