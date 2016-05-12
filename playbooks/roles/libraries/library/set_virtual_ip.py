#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import check_call, call, Popen, PIPE
from ansible.module_utils.basic import *

module = AnsibleModule(
    argument_spec=dict(
        ip=dict(required=True),
        device=dict(required=True),
    ),
)


def main():
    ip = module.params['ip']
    device = module.params['device']
    changed = set_vip(ip, device)
    module.exit_json(changed=changed)


def set_vip(ip, device):
    if get_vip(ip, device):
        return False
    cmd = ['ip', 'addr', 'add', '%s/32' % ip, 'dev', device]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        module.fail_json(msg=err)
    return True


def get_vip(ip, device):
    cmd = ['ip', 'addr', 'show', 'dev', device]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode != 0:
        module.fail_json(msg="ip addr show failed. stdout: %r" % output)
    if ' %s/32 ' % ip in output:
        return True
    return False


if __name__ == '__main__':
    main()
