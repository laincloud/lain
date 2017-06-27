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

wget -c https://github.com/laincloud/networkd/releases/download/v2.3.0/networkd -O playbooks/roles/networkd/files/networkd

wget -c https://github.com/laincloud/deployd/releases/download/v2.3.0/deployd -O playbooks/roles/deployd/files/deployd

wget -c https://github.com/laincloud/lainlet/releases/download/v2.0.5/lainlet -O playbooks/roles/lainlet/files/lainlet

wget -c https://github.com/projectcalico/calicoctl/releases/download/v1.2.1/calicoctl -O playbooks/roles/calico/files/bin/calicoctl

wget -c https://github.com/projectcalico/felix/releases/download/2.2.2/calico-felix -O playbooks/roles/calico/files/bin/calico-felix

wget -c https://github.com/projectcalico/bird/releases/download/v0.3.1/bird -O playbooks/roles/calico/files/bin/bird

wget -c https://github.com/projectcalico/bird/releases/download/v0.3.1/bird6 -O playbooks/roles/calico/files/bin/bird6

wget -c https://github.com/projectcalico/confd/releases/download/v0.11.2/confd -O playbooks/roles/calico/files/bin/confd

wget -c https://github.com/laincloud/libnetwork-plugin/releases/download/v1.1.0/libnetwork-plugin -O playbooks/roles/calico/files/bin/libnetwork-plugin

wget -c https://github.com/laincloud/calicoctl/releases/download/v1.2.1/allocate-ipip-addr -O playbooks/roles/calico/files/bin/allocate-ipip-addr

wget -c https://github.com/laincloud/calicoctl/releases/download/v1.2.1/startup -O playbooks/roles/calico/files/bin/startup
