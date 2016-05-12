#!/usr/bin/env python
# -*- coding: utf-8 -*-
# get app virtual ip from networkd config (etcd)
from subprocess import check_call, call, Popen, PIPE
from ansible.module_utils.basic import *

LAIN_VIP_PREFIX_KEY = "/lain/config/vips"

module = AnsibleModule(
    argument_spec=dict(
        container_app=dict(required=True),
        container_proc=dict(required=True),
        ),
)


def main():
    container_app = module.params['container_app']
    container_proc = module.params['container_proc']

    changed = False
    config = get_proc_config(app=container_app, proc=container_proc)
    if not config:
        module.fail_json(msg="No available virutual ip for %s %s" % (container_app, container_proc))
    ip = config.get("ip")
    if not ip:
        module.fail_json(msg="No available virutual ip for %s %s" % (container_app, container_proc))
    module.exit_json(changed=changed, ip=ip)


def get_proc_config(app, proc):
    keys = list_etcd_key(LAIN_VIP_PREFIX_KEY)
    if not keys:
        module.fail_json(msg="No available virtual ip configs")
    for key in keys:
        value = get_etcd_key(key)
        if not value:
            return None
        data = json.loads(value)
        config_app = data.get("app")
        if config_app != app:
            continue
        config_proc = data.get("proc")
        if config_proc != proc:
            continue
        data["ip"] = key[len(LAIN_VIP_PREFIX_KEY)+1:]
        return data


def list_etcd_key(key):
    p = Popen(['etcdctl', 'ls', key], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 4:
        if "Key not found" in err:
            return []
        else:
            module.fail_json(msg=err)
    elif p.returncode != 0:
        module.fail_json(msg=err)
    return output.rstrip().splitlines()


def get_etcd_key(key):
    p = Popen(['etcdctl', 'get', key], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 4:
        if "Key not found" in err:
            return None
        else:
            module.fail_json(msg=err)
    elif p.returncode != 0:
        module.fail_json(msg=err)
    return output.rstrip()


if __name__ == '__main__':
    main()
