#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import requests

from config import CONFIG


def test_registry_service(bootstrap):
    # verify return 200
    url = "http://" + CONFIG.vip + "/v2/"
    headers = {"Host": CONFIG.registry_hostname}
    req = requests.get(url, headers=headers)
    assert req.status_code == 200

    # verify there is something in registry
    url += "_catalog"
    req = requests.get(url, headers=headers)
    assert len(req.json()["repositories"]) > 0


def test_console_service(bootstrap):
    url = "http://" + CONFIG.vip + CONFIG.console_api_apps + "console/"
    headers = {"Host": CONFIG.console_hostname}
    req = requests.get(url, headers=headers)
    assert req.status_code == 200
