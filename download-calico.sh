#!/bin/sh

wget https://github.com/laincloud/networkd/releases/download/v0.1.22/networkd -O playbooks/roles/networkd-upgrade/files/networkd
wget https://github.com/laincloud/calico-upgrade/releases/download/v0.0.1/calico-upgrade -O playbooks/roles/calico-upgrade/files/bin/calico-upgrade
wget https://github.com/projectcalico/calicoctl/releases/download/v1.2.1/calicoctl -O playbooks/roles/calico-upgrade/files/bin/calicoctl
wget https://github.com/projectcalico/felix/releases/download/2.2.2/calico-felix -O playbooks/roles/calico-upgrade/files/bin/calico-felix
wget https://github.com/projectcalico/bird/releases/download/v0.3.1/bird -O playbooks/roles/calico-upgrade/files/bin/bird
wget https://github.com/projectcalico/bird/releases/download/v0.3.1/bird6 -O playbooks/roles/calico-upgrade/files/bin/bird6
wget https://github.com/projectcalico/confd/releases/download/v0.11.2/confd -O playbooks/roles/calico-upgrade/files/bin/confd
wget https://github.com/laincloud/libnetwork-plugin/releases/download/v1.1.0/libnetwork-plugin -O playbooks/roles/calico-upgrade/files/bin/libnetwork-plugin
wget https://github.com/laincloud/calicoctl/releases/download/v1.2.1/allocate-ipip-addr -O playbooks/roles/calico-upgrade/files/bin/allocate-ipip-addr