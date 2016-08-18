#!/usr/bin/env python

from subprocess import Popen, PIPE
import json
from ansible.module_utils.basic import *

module = AnsibleModule(
    argument_spec=dict(
        node=dict(required=True),
        app=dict(required=True),
        proc=dict(required=True),
        instance_number=dict(required=True),
        client_app=dict(),
    )
)

PORTAL_NETWORK_TEMPLATE = '%s.portal.%s_%s'
PORTAL_PROC_FILTER_TEMPLATE = '%s-%s-%s'
PROC_INSTANCE_FILTER_TEMPLATE = '-i%s-'


def main():
    appname = module.params['app']
    procname = module.params['proc']
    nodename = module.params['node']
    instance_no = module.params['instance_number']
    client_app = module.params['client_app']

    try:
        network_info = get_network_info(appname, procname, client_app)
        network_id = get_network_id(network_info)
        endpoint_id, container_ip = get_endpoint_info(
            network_info, nodename, procname, instance_no, client_app)
        module.exit_json(changed=False, network_id=network_id,
                         endpoint_id=endpoint_id, recycle_ip=container_ip)
    except Exception as e:
        module.fail_json(msg=str(e))


def get_network_info(appname, procname, client_app):
    network = PORTAL_NETWORK_TEMPLATE % (
        appname, procname, client_app) if client_app else appname

    p = Popen(['docker', 'network', 'inspect', network],
              stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        module.fail_json(msg=err)
    return json.loads(output.rstrip())


def get_network_id(network_info):
    return network_info[0]['Id']


def get_endpoint_info(network_info, nodename, procname, instance_no, client_app):
    containers_info = network_info[0]['Containers']
    endpoint_id, container_ip = None, None
    for k, v in containers_info.iteritems():
        container_name = v['Name']
        if match_proc_info(container_name, nodename, procname, instance_no, client_app):
            endpoint_id = v['EndpointID']
            # the format of ip is 'x.x.x.x/32'
            container_ip = v['IPv4Address']
    if container_ip is None:
        raise Exception("fail to parse container ip")
    return endpoint_id, container_ip[0:len(container_ip) - 3]


def match_proc_info(container_name, nodename, procname, instance_no, client_app):
    proc_filter = PORTAL_PROC_FILTER_TEMPLATE % (
        procname, nodename, client_app) if client_app else procname
    instance_filter = PROC_INSTANCE_FILTER_TEMPLATE % instance_no

    instance_info = container_name.split('.')[-1]
    procname_info = container_name.split('.')[-2]
    return proc_filter in procname_info and instance_filter in instance_info


if __name__ == '__main__':
    main()
