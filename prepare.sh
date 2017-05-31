#!/bin/sh

filename="lain-pre-1495082869.tar.gz"
if [ ! -f "$filename" ]; then
    wget https://lain.oss-cn-beijing.aliyuncs.com/${filename}
fi
pre_dir=playbooks/roles/binary/files/
[ -d $pre_dir ] || mkdir $pre_dir
tar -xzvf $filename -C playbooks/roles/binary/files/

wget https://github.com/laincloud/networkd/releases/download/v0.1.21/networkd -O playbooks/roles/networkd-upgrade/files/networkd
wget https://github.com/laincloud/calico-upgrade/releases/download/v0.0.1/calico-upgrade -O playbooks/roles/calico-upgrade/files/bin/calico-upgrade
wget https://github.com/projectcalico/calicoctl/releases/download/v1.2.1/calicoctl -O playbooks/roles/calico-upgrade/files/bin/calicoctl