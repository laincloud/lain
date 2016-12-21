#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import requests
from config import CONFIG


def reposit(app_name):
    url = "http://" + CONFIG.vip + CONFIG.console_api_repos
    payload = {"appname": app_name}
    headers = {
        "Host": CONFIG.console_hostname,
        "Content-Type": "application/json"
    }
    return requests.post(url, json=payload, headers=headers)


def deploy(app_name):
    url = "http://" + CONFIG.vip + CONFIG.console_api_apps
    payload = {"appname": app_name}
    headers = {
        "Host": CONFIG.console_hostname,
        "Content-Type": "application/json"
    }
    return requests.post(url, json=payload, headers=headers)


def delete(app_name):
    url = "http://" + CONFIG.vip + CONFIG.console_api_apps + app_name + "/"
    headers = {"Host": CONFIG.console_hostname}
    return requests.delete(url, headers=headers)


def scale(app_name, proc_name, num_instances):
    url = "http://" + CONFIG.vip + CONFIG.console_api_apps + app_name + \
          "/procs/" + proc_name + "/"
    payload = {"num_instances": num_instances}
    headers = {
        "Host": CONFIG.console_hostname,
        "Content-Type": "application/json"
    }
    return requests.patch(url, json=payload, headers=headers)


def get_proc_info(app_name, proc_name):
    url = "http://" + CONFIG.vip + CONFIG.console_api_apps + app_name + \
          "/procs/" + proc_name + "/"
    headers = {"Host": CONFIG.console_hostname}
    return requests.get(url, headers=headers)
