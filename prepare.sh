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

if [ ! -f "playbooks/roles/networkd/files/networkd" ]; then
    wget https://github.com/laincloud/networkd/releases/download/v0.1.22/networkd -O playbooks/roles/networkd/files/networkd
fi

if [ ! -f "playbooks/roles/calico/files/bin/calicoctl" ]; then
    wget https://github.com/projectcalico/calicoctl/releases/download/v1.2.1/calicoctl -O playbooks/roles/calico/files/bin/calicoctl
fi

if [ ! -f "playbooks/roles/calico/files/bin/calico-felix" ]; then
    wget https://github.com/projectcalico/felix/releases/download/2.2.2/calico-felix -O playbooks/roles/calico/files/bin/calico-felix
fi

if [ ! -f "playbooks/roles/calico/files/bin/bird" ]; then
    wget https://github.com/projectcalico/bird/releases/download/v0.3.1/bird -O playbooks/roles/calico/files/bin/bird
fi

if [ ! -f "playbooks/roles/calico/files/bin/bird6" ]; then
    wget https://github.com/projectcalico/bird/releases/download/v0.3.1/bird6 -O playbooks/roles/calico/files/bin/bird6
fi

if [ ! -f "playbooks/roles/calico/files/bin/confd" ]; then
    wget https://github.com/projectcalico/confd/releases/download/v0.11.2/confd -O playbooks/roles/calico/files/bin/confd
fi

if [ ! -f "playbooks/roles/calico/files/bin/libnetwork-plugin" ]; then
    wget https://github.com/laincloud/libnetwork-plugin/releases/download/v1.1.0/libnetwork-plugin -O playbooks/roles/calico/files/bin/libnetwork-plugin
fi

if [ ! -f "playbooks/roles/calico/files/bin/allocate-ipip-addr" ]; then
    wget https://github.com/laincloud/calicoctl/releases/download/v1.2.1/allocate-ipip-addr -O playbooks/roles/calico/files/bin/allocate-ipip-addr
fi

if [ ! -f "playbooks/roles/calico/files/bin/startup" ]; then
    wget https://github.com/laincloud/calicoctl/releases/download/v1.2.1/startup -O playbooks/roles/calico/files/bin/startup
fi
