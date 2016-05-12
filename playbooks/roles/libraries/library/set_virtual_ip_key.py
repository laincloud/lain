#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import check_call, call, Popen, PIPE
from ansible.module_utils.basic import *

LAIN_VIP_PREFIX_KEY = "/lain/config/vips"

module = AnsibleModule(
    argument_spec=dict(
        ip=dict(required=True),
        port=dict(required=True),
        container_app=dict(required=True),
        container_proc=dict(required=True),
        container_port=dict(),
        container_proto=dict(),
        ),
)


def main():
    ip = module.params['ip']
    port = module.params['port']
    container_port = module.params['container_port']
    container_proto = module.params['container_proto']
    container_app = module.params['container_app']
    container_proc = module.params['container_proc']

    changed = False
    config = {
        "app": container_app,
        "proc": container_proc,
    }

    if container_proto:
        config["proto"] = container_proto
    else:
        config["proto"] = "tcp"

    if container_port:
        config["port"] = container_port
    else:
        config["port"] = port

    old_config = get_config(ip, port)
    if not old_config:
        changed = True
    else:
        for item in ['app', 'proc']:
            if config.get(item) != old_config.get(item):
                changed = True
        if not changed:
            key = "%s-%s-%s" % (port, config["proto"], config["port"])
            if key not in old_config["ports"]:
                changed = True

    if changed is False:
        module.exit_json(changed=changed)

    set_config(ip, port, config)
    module.exit_json(changed=changed)


def get_config(ip, port):
    if ip == "0.0.0.0":
        key = "%s/%s:%s" % (LAIN_VIP_PREFIX_KEY, ip, port)
    else:
        key = "%s/%s" % (LAIN_VIP_PREFIX_KEY, ip)
    value = get_etcd_key(key)
    if value is None:
        return None
    elif value == "":
        return None
    data = json.loads(value)
    port_configs = data.get("ports", [])
    index_ports = {}
    for config in port_configs:
        src = config["src"]
        proto = config.get("proto", "tcp")
        dest = config.get("dest", src)
        key = "%s-%s-%s" % (src, proto, dest)
        index_ports[key] = True
    data["ports"] = index_ports
    return data


def set_config(ip, port, data):
    if ip == "0.0.0.0":
        key = "%s/%s:%s" % (LAIN_VIP_PREFIX_KEY, ip, port)
    else:
        key = "%s/%s" % (LAIN_VIP_PREFIX_KEY, ip)
    prev_value = get_etcd_key(key)
    prev_data = json.loads(prev_value) if prev_value else {}
    prev_data["app"] = data["app"]
    prev_data["proc"] = data["proc"]
    ports = prev_data.get("ports", [])
    ports.append({"src": port, "proto": data["proto"], "dest": data["port"]})
    prev_data["ports"] = ports
    value = json.dumps(prev_data)
    set_etcd_key(key, value, prev_value)


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


def set_etcd_key(key, value, prev_value=None):
    if prev_value is not None:
        cmd = ['etcdctl', 'set', key, value, '--swap-with-value', prev_value]
    else:
        cmd = ['etcdctl', 'set', key, value]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        module.fail_json(msg=err)


if __name__ == '__main__':
    main()
