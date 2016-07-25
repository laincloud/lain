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

    try:
        subnet_key_list = get_assign_subnet_keys()
        subnet_key = get_subnet_key_of_ip(ip, subnet_key_list)
        module.exit_json(changed=recycle_ip(ip, subnet_key))
    except Exception as e:
        module.fail_json(msg=str(e))


def get_assign_subnet_keys():
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


def get_subnet_key_of_ip(ip, subnet_key_list):
    ipaddr = ip_address(ip)
    for subnet_key in subnet_key_list:
        subnet = subnet_key[len(IP_ASSIGN_KEY):len(subnet_key)].replace('-', '/')
        if ipaddr in IPv4Network(subnet):
            return subnet_key
    module.fail_json(msg='find proper subnet wrong!')


def recycle_ip(ip, subnet_key):
    try:
        assign_info = adjust_ip_assign_info(ip, subnet_key)
        p = Popen(['etcdctl', 'set', subnet_key, assign_info],
                  stdout=PIPE, stderr=PIPE)
        _, err = p.communicate()
        if p.returncode != 0:
            module.fail_json(msg=err)
        return True
    except Exception, e:
        module.fail_json(msg=str(e))


def adjust_ip_assign_info(ip, subnet_key):
    assign_info = get_ip_assign_info(ip, subnet_key)
    subnet = assign_info['cidr']

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

    # if only assigned the recycling ip, set the `attributes` param to be empty
    if assign_count == 1:
        assign_info['attributes'] = []

    return json.dumps(assign_info)


def get_ip_assign_info(ip, subnet_key):
    p = Popen(['etcdctl', 'get', subnet_key], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 4:
        if "Key not found" in err:
            return []
        else:
            module.fail_json(msg=err)
    elif p.returncode != 0:
        module.fail_json(msg=err)
    return json.loads(output.rstrip())


if __name__ == "__main__":
    main()
