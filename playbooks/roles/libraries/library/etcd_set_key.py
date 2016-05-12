#!/usr/bin/python

from urllib2 import urlopen, HTTPError
import json
from subprocess import check_call


def main():
    module = AnsibleModule(
        argument_spec=dict(
            key=dict(required=True),
            value=dict(required=True),
            etcd_client_port=dict(default="4001"),
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
        check_call(['etcdctl', 'set', key, value])

    current_value = get_key(key)

    if current_value == value:
        module.exit_json(changed=False)

    set_key(key, value)
    module.exit_json(changed=True)


from ansible.module_utils.basic import *
main()
