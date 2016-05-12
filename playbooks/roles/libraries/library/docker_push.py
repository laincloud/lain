#!/usr/bin/env python

from subprocess import check_call
from urllib2 import urlopen, HTTPError


def main():
    module = AnsibleModule(
        argument_spec=dict(
            image=dict(required=True),
            registry=dict(required=True),
        ),
    )

    image = module.params['image']
    registry = module.params['registry']

    repo, tag = image.rsplit(':', 1)
    url = 'http://%s/v2/%s/manifests/%s' % (registry, repo, tag)
    try:
        urlopen(url)
    except HTTPError as e:
        if e.code != 404:
            raise
    else:
        # already in registry
        module.exit_json(changed=False)

    target = '%s/%s' % (registry, image)
    check_call(['docker', 'tag', image, target])
    check_call(['docker', 'push', target])
    module.exit_json(changed=True)


from ansible.module_utils.basic import *
main()
