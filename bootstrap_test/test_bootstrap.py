#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
import time

import requests
import pytest

import app_ctl

APPNAME = "hello"

IMAGE_NAME = "swarm"

def test_registry_service(bootstrap):
    # verify return 404
    headers={"Host": "registry" + app_ctl.DOMAIN}
    req = requests.get(app_ctl.VIP, headers=headers)
    assert req.status_code == 404

    # verify something in registry
    url = app_ctl.VIP + "/v2/" + IMAGE_NAME + "/tags/list"
    req = requests.get(url, headers=headers)
    content = json.loads(req.text)
    assert content["name"] == IMAGE_NAME

def test_console_service(bootstrap):
    headers={"Host": app_ctl.CONSOLE_ADDRESS}
    req = requests.get(app_ctl.VIP, headers=headers)
    assert req.status_code == 200
