#!/usr/bin/env python

from urllib2 import Request, urlopen, HTTPError
import json


def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(required=True),
            body=dict(required=True),
            header=dict(required=False),
        )
    )

    url = module.params['url']
    body = module.params['body']
    header = module.params['header']

    req = Request(url)
    req.add_header('Content-Type', 'application/json')
    if header:
        for k, v in header.iteritems():
            req.add_header(k, v)

    try:
        urlopen(req, json.dumps(body))
    except HTTPError as e:
        module.fail_json(msg=e.reason, code=e.code, response=e.read())
    else:
        module.exit_json(changed=True)

from ansible.module_utils.basic import *
main()
