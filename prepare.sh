#!/bin/sh

set -e

NETWORKD_VERSION="v2.3.1"
DEPLOYD_VERSION="v2.3.1"
LAINLET_VERSION="v2.3.3"
CALICOCTL_VERSION="v1.2.2"
ALLOCATE_IPIP_ADDR_VERSION="v1.2.2"
STARTUP_VERSION="v1.2.2"
CALICO_FELIX_VERSION="2.2.2"
CONFD_VERSION="v0.11.2"
LIBNETWORK_PLUGIN_VERSION="v1.1.0"
BIRD_VERSION="v0.3.1"
BIRD6_VERSION="v0.3.1"
CONSUL_VERSION="0.8.5"
ETCD_VERSION="2.3.7"
BINARY_URL_PREFIX="https://lain.oss-cn-beijing.aliyuncs.com/binary"

filename="lain-pre-1476939656.tar.gz"
if [ ! -f "$filename" ]; then
    wget https://lain.oss-cn-beijing.aliyuncs.com/${filename}
fi
pre_dir=playbooks/roles/binary/files/
[ -d $pre_dir ] || mkdir $pre_dir
tar -xzvf $filename -C playbooks/roles/binary/files/

mkdir -p playbooks/roles/networkd/files
mkdir -p playbooks/roles/deployd/files
mkdir -p playbooks/roles/lainlet/files
mkdir -p playbooks/roles/calico/files/bin
mkdir -p playbooks/roles/consul/files/bin

wget  ${BINARY_URL_PREFIX}/networkd/releases/download/${NETWORKD_VERSION}/networkd.xz -O playbooks/roles/networkd/files/networkd.xz
wget  ${BINARY_URL_PREFIX}/deployd/releases/download/${DEPLOYD_VERSION}/deployd.xz -O playbooks/roles/deployd/files/deployd.xz
wget  ${BINARY_URL_PREFIX}/lainlet/releases/download/${LAINLET_VERSION}/lainlet.xz -O playbooks/roles/lainlet/files/lainlet.xz
wget  ${BINARY_URL_PREFIX}/calicoctl/releases/download/${CALICOCTL_VERSION}/calicoctl.xz -O playbooks/roles/calico/files/bin/calicoctl.xz
wget  ${BINARY_URL_PREFIX}/calicoctl/releases/download/${ALLOCATE_IPIP_ADDR_VERSION}/allocate-ipip-addr.xz -O playbooks/roles/calico/files/bin/allocate-ipip-addr.xz
wget  ${BINARY_URL_PREFIX}/calicoctl/releases/download/${STARTUP_VERSION}/startup.xz -O playbooks/roles/calico/files/bin/startup.xz
wget  ${BINARY_URL_PREFIX}/felix/releases/download/${CALICO_FELIX_VERSION}/calico-felix.xz -O playbooks/roles/calico/files/bin/calico-felix.xz
wget  ${BINARY_URL_PREFIX}/confd/releases/download/${CONFD_VERSION}/confd.xz -O playbooks/roles/calico/files/bin/confd.xz
wget  ${BINARY_URL_PREFIX}/libnetwork-plugin/releases/download/${LIBNETWORK_PLUGIN_VERSION}/libnetwork-plugin.xz -O playbooks/roles/calico/files/bin/libnetwork-plugin.xz
wget  ${BINARY_URL_PREFIX}/bird/releases/download/${BIRD_VERSION}/bird.xz -O playbooks/roles/calico/files/bin/bird.xz
wget  ${BINARY_URL_PREFIX}/bird/releases/download/${BIRD6_VERSION}/bird6.xz -O playbooks/roles/calico/files/bin/bird6.xz
wget  ${BINARY_URL_PREFIX}/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip -O playbooks/roles/consul/files/bin/consul_${CONSUL_VERSION}_linux_amd64.zip
wget  http://lain.oss-cn-beijing.aliyuncs.com/etcd-${ETCD_VERSION}-4.el7.x86_64.rpm -O playbooks/roles/etcd/files/etcd-${ETCD_VERSION}-4.el7.x86_64.rpm


unxz -kf playbooks/roles/networkd/files/networkd.xz
unxz -kf playbooks/roles/deployd/files/deployd.xz
unxz -kf playbooks/roles/lainlet/files/lainlet.xz
unxz -kf playbooks/roles/calico/files/bin/calicoctl.xz
unxz -kf playbooks/roles/calico/files/bin/allocate-ipip-addr.xz
unxz -kf playbooks/roles/calico/files/bin/startup.xz
unxz -kf playbooks/roles/calico/files/bin/calico-felix.xz
unxz -kf playbooks/roles/calico/files/bin/confd.xz
unxz -kf playbooks/roles/calico/files/bin/libnetwork-plugin.xz
unxz -kf playbooks/roles/calico/files/bin/bird.xz
unxz -kf playbooks/roles/calico/files/bin/bird6.xz
unzip -o playbooks/roles/consul/files/bin/consul_${CONSUL_VERSION}_linux_amd64.zip -d playbooks/roles/consul/files/bin
