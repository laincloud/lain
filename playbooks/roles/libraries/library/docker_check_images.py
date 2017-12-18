#!/usr/bin/python

from subprocess import Popen, PIPE

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            images=dict(type='list', required=True),
        ),
    )

    images = module.params['images']

    p = Popen(['docker', 'inspect', '-f', '{{.Id}}'] + images, stderr=PIPE)
    stderr = p.stderr.read()
    if p.wait() == 0:
        module.exit_json(changed=False)
    else:
        module.fail_json(msg=stderr)


if __name__ == '__main__':
    main()
