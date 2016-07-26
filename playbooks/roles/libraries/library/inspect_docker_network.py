#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
from ansible.module_utils.basic import *

module = AnsibleModule(
    argument_spec=dict(
        app=dict(required=True),
        proc=dict(required=True),
        instance_number=dict(required=True),
    )
)


def main():
    appname = module.params['app']
    procname = module.params['proc']
    instance_no = module.params['instance_number']

    try:
        network_info = get_network_info(appname)
        network_id = get_network_id(network_info)
        endpoint_id, container_ip = get_endpoint_info(
            network_info, procname, instance_no)
        module.exit_json(changed=False, network_id=network_id,
                         endpoint_id=endpoint_id, recycle_ip=container_ip)
    except Exception as e:
        module.fail_json(msg=str(e))


def get_network_info(appname):
    p = Popen(['docker', 'network', 'inspect', appname],
              stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        module.fail_json(msg=err)
    return json.loads(output.rstrip())


def get_network_id(network_info):
    return network_info[0]['Id']


def get_endpoint_info(network_info, procname, instance_no):
    containers_info = network_info[0]['Containers']
    endpoint_id, container_ip = None, None
    for k, v in containers_info.iteritems():
        container_name = v['Name']
        if match_proc_instance(container_name, procname, instance_no):
            endpoint_id = v['EndpointID']
            container_ip = v['IPv4Address']    # the format of ip is 'x.x.x.x/32'
    return endpoint_id, container_ip[0:len(container_ip) - 3]


# container name should include procname and instance no
def match_proc_instance(name, procname, instance_no):
    instance_filter = '-i' + instance_no + '-'
    return procname in name and instance_filter in name


if __name__ == '__main__':
    main()
