#!/bin/sh

set -e

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

wget -c https://github.com/laincloud/networkd/releases/download/v2.3.0/networkd.xz -O playbooks/roles/networkd/files/networkd.xz

wget -c https://github.com/laincloud/deployd/releases/download/v2.3.0/deployd.xz -O playbooks/roles/deployd/files/deployd.xz

wget -c https://github.com/laincloud/lainlet/releases/download/v2.3.0/lainlet.xz -O playbooks/roles/lainlet/files/lainlet.xz

wget -c https://github.com/laincloud/calicoctl/releases/download/v1.2.1/calicoctl.xz -O playbooks/roles/calico/files/bin/calicoctl.xz

wget -c https://github.com/laincloud/calicoctl/releases/download/v1.2.1/allocate-ipip-addr.xz -O playbooks/roles/calico/files/bin/allocate-ipip-addr.xz

wget -c https://github.com/laincloud/calicoctl/releases/download/v1.2.1/startup.xz -O playbooks/roles/calico/files/bin/startup.xz

wget -c https://github.com/laincloud/felix/releases/download/2.2.2/calico-felix.xz -O playbooks/roles/calico/files/bin/calico-felix.xz

wget -c https://github.com/laincloud/confd/releases/download/v0.11.2/confd.xz -O playbooks/roles/calico/files/bin/confd.xz

wget -c https://github.com/laincloud/libnetwork-plugin/releases/download/v1.1.0/libnetwork-plugin.xz -O playbooks/roles/calico/files/bin/libnetwork-plugin.xz

wget -c https://github.com/projectcalico/bird/releases/download/v0.3.1/bird -O playbooks/roles/calico/files/bin/bird

wget -c https://github.com/projectcalico/bird/releases/download/v0.3.1/bird6 -O playbooks/roles/calico/files/bin/bird6

wget -c https://releases.hashicorp.com/consul/0.8.5/consul_0.8.5_linux_amd64.zip -O playbooks/roles/consul/files/bin/consul_0.8.5_linux_amd64.zip

unxz -kf playbooks/roles/networkd/files/networkd.xz
unxz -kf playbooks/roles/deployd/files/deployd.xz
unxz -kf playbooks/roles/lainlet/files/lainlet.xz
unxz -kf playbooks/roles/calico/files/bin/calicoctl.xz
unxz -kf playbooks/roles/calico/files/bin/allocate-ipip-addr.xz
unxz -kf playbooks/roles/calico/files/bin/startup.xz
unxz -kf playbooks/roles/calico/files/bin/calico-felix.xz
unxz -kf playbooks/roles/calico/files/bin/confd.xz
unxz -kf playbooks/roles/calico/files/bin/libnetwork-plugin.xz
unzip -o playbooks/roles/consul/files/bin/consul_0.8.5_linux_amd64.zip -d playbooks/roles/consul/files/bin
