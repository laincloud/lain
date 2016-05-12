#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
import time

import requests

import app_ctl

APPNAME = "hello"
PROCNAME = "web"
NUM_INSTANCES = 4

def test_deploy_hello(prepare_demo_images):
    app_ctl.delete(APPNAME)
    app_ctl.reposit(APPNAME)
    req = app_ctl.deploy(APPNAME)
    # print(req.text)
    assert req.status_code == 201
    content = json.loads(req.text)
    assert "OK: True" in content['msg']

    assert app_ctl.is_working(APPNAME) == True
    req = app_ctl.get_service(APPNAME)
    assert req.status_code == 200
    assert req.text == 'Hello, "/"'
    # print(content['msg'])

    req = app_ctl.delete(APPNAME)
    assert req.status_code == 202

def test_scale_app(prepare_demo_images, add_node):
    app_ctl.delete(APPNAME)
    app_ctl.reposit(APPNAME)
    app_ctl.deploy(APPNAME)
    assert app_ctl.is_working(APPNAME) == True

    req = app_ctl.scale(APPNAME, PROCNAME, NUM_INSTANCES)
    assert req.status_code == 202
    assert app_ctl.is_scaled(APPNAME, PROCNAME, NUM_INSTANCES) == True

    for i in range(NUM_INSTANCES):
        req = app_ctl.get_service(APPNAME)
        assert req.status_code == 200
        assert req.text == 'Hello, "/"'

    app_ctl.delete(APPNAME)
