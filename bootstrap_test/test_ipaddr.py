#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import requests

import app_ctl
from config import CONFIG


def test_client_is_working(deploy_ipaddr):
    url = "http://" + CONFIG.vip
    headers = {"Host": CONFIG.ipaddr_client_hostname}
    req = requests.get(url, headers=headers)
    assert req.status_code == 200


def test_client_is_scaled(scale_ipaddr_client):
    req = app_ctl.get_proc_info(CONFIG.ipaddr_client_appname,
                                CONFIG.ipaddr_client_procname)
    assert len(req.json()['proc'][
        'pods']) == CONFIG.ipaddr_client_num_instances
