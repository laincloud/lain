#!/usr/bin/python

from urllib2 import urlopen, HTTPError
import json
import os
from subprocess import check_call

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            key=dict(type='str', required=True),
            value=dict(type='str', required=True),
            etcd_client_port=dict(type='str', default="4001"),
        ),
    )

    key = module.params['key']
    value = module.params['value']
    endpoint = "http://127.0.0.1:%s" % module.params['etcd_client_port']

    def get_key(key):
        try:
            f = urlopen('%s/v2/keys%s' % (endpoint, key))
        except HTTPError as e:
            if e.code == 404:
                return None
            raise

        data = json.load(f)
        return data['node']['value']

    def set_key(key, value):
        with open(os.devnull, 'w') as fnull:
            check_call(['etcdctl', 'set', key, value], stdout=fnull)

    current_value = get_key(key)

    if current_value == value:
        module.exit_json(changed=False)

    set_key(key, value)

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
