#!/usr/bin/python

from subprocess import Popen, PIPE


def main():
    module = AnsibleModule(
        argument_spec=dict(
            images=dict(required=True),
        ),
    )

    images = module.params['images']

    p = Popen(['docker', 'inspect', '-f', '{{.Id}}'] + images, stderr=PIPE)
    stderr = p.stderr.read()
    if p.wait() == 0:
        module.exit_json(changed=False)
    else:
        module.fail_json(msg=stderr)


from ansible.module_utils.basic import *

main()
