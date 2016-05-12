#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json

import requests
from retrying import retry

VIP = "http://192.168.77.254"
CONSOLE_API = "/api/v1/apps/"
REPOSIT_API = "/api/v1/repos/"
DOMAIN = ".lain.local"
CONSOLE_ADDRESS = "console" + DOMAIN

WAIT_INTERVAL_MIN = 10000  # unit: millisecond
WAIT_INTERVAL_MAX = 20000  # unit: millisecond
TIME_OUT = 240000  # unit: millisecond

class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def reposit(app_name):
    url = VIP + REPOSIT_API
    headers = {"Host": CONSOLE_ADDRESS, "Content-Type": "application/json"}
    app_info = json.dumps({"appname": app_name})
    return requests.post(url, data=app_info, headers=headers)

def deploy(app_name):
    url = VIP + CONSOLE_API
    headers = {"Host": CONSOLE_ADDRESS, "Content-Type": "application/json"}
    app_info = json.dumps({"appname": app_name})
    return requests.post(url, data=app_info, headers=headers)

def delete(app_name):
    url = VIP + CONSOLE_API + app_name + "/"
    headers = {"Host": CONSOLE_ADDRESS}
    return requests.delete(url, headers=headers)

def scale(app_name, proc_name, num_instances):
    url = VIP + CONSOLE_API + app_name + "/procs/" + \
            proc_name + "/"
    headers = {"Host": CONSOLE_ADDRESS, "Content-Type": "application/json"}
    app_info = json.dumps({"num_instances": num_instances})
    return requests.patch(url, data=app_info, headers=headers)

def get_service(app_name):
    headers = {"Host": app_name + DOMAIN}
    return requests.get(VIP, headers=headers)

def get_proc_info(app_name, proc_name):
    url = VIP + CONSOLE_API + app_name + "/procs/" + \
            proc_name + "/"
    headers = {"Host": CONSOLE_ADDRESS}
    return requests.get(url, headers=headers)

@retry(wait_random_min=WAIT_INTERVAL_MIN, wait_random_max=WAIT_INTERVAL_MAX, stop_max_delay=TIME_OUT)
def is_working(app_name):
    req = get_service(app_name)
    if req.text != 'Hello, "/"':
        raise MyError("app not working yet")
    else:
        return True

@retry(wait_random_min=WAIT_INTERVAL_MIN, wait_random_max=WAIT_INTERVAL_MAX, stop_max_delay=TIME_OUT)
def is_scaled(app_name, proc_name, num_instances):
    req = get_proc_info(app_name, proc_name)
    content = json.loads(req.text)
    if len(content['proc']['pods']) != num_instances:
        raise MyError("scale not ready yet")
    else:
        return True

