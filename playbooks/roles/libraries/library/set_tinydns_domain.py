#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from ansible.module_utils.basic import *

LAIN_TINYDNS_PREFIX_KEY = "/lain/config/tinydns_fqdns"

module = AnsibleModule(
    argument_spec=dict(
        domain=dict(required=True),
        record=dict(required=True),
    ),
)


def main():

    domain = module.params['domain']
    record = module.params['record']
    changed = False

    old_config = get_config(domain)
    if not old_config:
        if record == "":
            module.exit_json(changed=changed)
        changed = True
    else:
        if len(old_config) > 1:
            changed = True
        elif old_config[0] != record:
            changed = True

    if changed is False:
        module.exit_json(changed=changed)

    set_config(domain, record)
    module.exit_json(changed=changed)


def get_config(domain):
    key = "%s/%s" % (LAIN_TINYDNS_PREFIX_KEY, domain)
    value = get_etcd_key(key)

    if value is None:
        return None
    elif value == "":
        return None
    data = json.loads(value)
    return data


def set_config(domain, record):
    key = "%s/%s" % (LAIN_TINYDNS_PREFIX_KEY, domain)
    if record == "":
        rm_etcd_key(key)
        return
    data = [record]
    value = json.dumps(data)
    prev_value = get_etcd_key(key)
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


def rm_etcd_key(key):
    cmd = ['etcdctl', 'rm', key]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        module.fail_json(msg=err)


if __name__ == '__main__':
    main()
