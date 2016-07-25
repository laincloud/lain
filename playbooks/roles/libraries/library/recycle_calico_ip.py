#!/usr/bin/env python

from ipaddress import ip_address, IPv4Network
from subprocess import Popen, PIPE
from ansible.module_utils.basic import *
import json

IP_ASSIGN_KEY = '/calico/ipam/v2/assignment/ipv4/block/'

module = AnsibleModule(
    argument_spec=dict(
        ip=dict(required=True),
    )
)

def main():

    ip = module.params['ip']
    subnet_list = get_subnet_list()
    ip_subnet = get_subnet_of_ip(ip, subnet_list)

    try:
        module.exit_json(changed=recycle_ip(ip, ip_subnet))
    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=True)


def get_subnet_list():
    p = Popen(['etcdctl', 'ls', IP_ASSIGN_KEY], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 4:
        if "Key not found" in err:
            return []
        else:
            module.fail_json(msg=err)
    elif p.returncode != 0:
        module.fail_json(msg=err)
    return output.rstrip().splitlines()


def get_subnet_of_ip(ip, subnet_list):
    ipaddr = ip_address(ip)
    for subnet in subnet_list:
        if ipaddr in IPv4Network(subnet[len(IP_ASSIGN_KEY):len(subnet)].replace('-', '/')):
            return subnet
    module.fail_json(msg='find proper subnet wrong!')


def recycle_ip(ip, ip_subnet):
    try:    
        assign_info = adjust_ip_assign_info(ip, ip_subnet)
        p = Popen(['etcdctl', 'set', ip_subnet, assign_info], stdout=PIPE, stderr=PIPE)
        _, err = p.communicate()
        if p.returncode != 0:
            module.fail_json(msg=err)
        return True
    except Exception, e:
        module.fail_json(msg=str(e))


def adjust_ip_assign_info(ip, ip_subnet):
    assign_info = json.loads(get_ip_assign_info(ip, ip_subnet))

    subnet = assign_info.get('cidr', None)
    assign_count, index, ip_index = 0, 0, -1
    for addr in IPv4Network(subnet):
        if assign_info['allocations'][index] == 0 or assign_info['allocations'][index] == 1:
            assign_count += 1
            if addr == ip_address(ip):
                ip_index = index
        index += 1

    if ip_index != -1:
        assign_info['allocations'][ip_index] = None
        assign_info['unallocated'].append(ip_index)

    if assign_count == 1:
        assign_info['attributes'] = []

    return json.dumps(assign_info)


def get_ip_assign_info(ip, ip_subnet):
    key = ip_subnet
    p = Popen(['etcdctl', 'get', key], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 4:
        if "Key not found" in err:
            return []
        else:
            module.fail_json(msg=err)
    elif p.returncode != 0:
        module.fail_json(msg=err)
    return output.rstrip()

if __name__ == "__main__":
    main()
