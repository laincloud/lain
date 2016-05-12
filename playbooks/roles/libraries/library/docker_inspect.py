#!/usr/bin/env python

import docker
from docker.errors import APIError


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            type=dict(default='container', choices=['container', 'image']),
        ),
    )

    name = module.params['name']
    type = module.params['type']

    client = docker.Client()

    if type == 'container':
        inspect_method = client.inspect_container
    elif type == 'image':
        inspect_method = client.inspect_image
    else:
        # should not reach here
        raise Exception("unknown type")

    try:
        result = inspect_method(name)
    except APIError as e:
        if e.response.status_code == 404:
            module.fail_json(msg="%s does not exists" % name)
        raise

    result['changed'] = False
    module.exit_json(**result)


from ansible.module_utils.basic import *
main()
