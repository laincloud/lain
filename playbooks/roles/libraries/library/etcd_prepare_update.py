#!/usr/bin/python

import os
from subprocess import check_call

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            current_members=dict(type='list', required=True),
            wanted_members=dict(type='list', required=True),
            is_lain_manager=dict(type='bool', required=True),
            node_name=dict(type='str', required=True)
        ),
    )

    current_members = module.params['current_members']
    wanted_members = module.params['wanted_members']
    is_lain_manager = module.params['is_lain_manager']
    node_name = module.params['node_name']

    if len(set(current_members).symmetric_difference(set(wanted_members))) > 1:
        module.fail_json(msg="you can only remove or add one node a time.")

    msg = 'skip etcd backup'
    if is_lain_manager:
        with open(os.devnull, 'w') as fnull:
            data_dir = '/var/etcd/%s' % node_name
            tmp_dir = '/tmp/lain/etcd_backup/'
            check_call(['rm', '-rf', tmp_dir], stdout=fnull)
            check_call(['etcdctl', 'backup', '--data-dir', data_dir, '--backup-dir', tmp_dir], stdout=fnull)
            msg = "backup etcd to %s successfully" % tmp_dir
    module.exit_json(changed=True, msg=msg)


if __name__ == '__main__':
    main()
