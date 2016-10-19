#!/usr/bin/python

from subprocess import call, check_call


def main():
    module = AnsibleModule(
        argument_spec=dict(
            image=dict(required=True),
            registry=dict(default=''),
        ),
    )

    image = module.params['image']
    registry = module.params['registry']

    retval = call(['docker', 'inspect', '-f', '{{.Id}}', image])
    if retval == 0:
        # image already exists
        module.exit_json(changed=False)

    if registry:
        src_image = '%s/%s' % (registry, image)
        check_call(['docker', 'pull', src_image])
        check_call(['docker', 'tag', src_image, image])
    else:
        check_call(['docker', 'pull', image])

    module.exit_json(changed=True)

from ansible.module_utils.basic import *

main()
