#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import yaml


class Config(object):
    def __init__(self):
        config_file_path = os.path.join(os.path.dirname(__file__),
                                        'config.yaml')
        with open(config_file_path, 'r') as f:
            self._config = yaml.safe_load(f)

    @property
    def vip(self):
        return self._config["vip"]

    @property
    def domain(self):
        return self._config["domain"]

    @property
    def console_hostname(self):
        return "console." + self.domain

    @property
    def registry_hostname(self):
        return "registry." + self.domain

    @property
    def console_api_repos(self):
        return self._config["console_api"]["repos"]

    @property
    def console_api_apps(self):
        return self._config["console_api"]["apps"]

    @property
    def ipaddr(self):
        return self._config["ipaddr"]

    @property
    def ipaddr_service_appname(self):
        return self.ipaddr["service"]["appname"]

    @property
    def ipaddr_resource_appname(self):
        return self.ipaddr["resource"]["appname"]

    @property
    def ipaddr_client_appname(self):
        return self.ipaddr["client"]["appname"]

    @property
    def ipaddr_client_procname(self):
        return self.ipaddr["client"]["procname"]

    @property
    def ipaddr_client_num_instances(self):
        return self.ipaddr["client"]["num_instances"]

    @property
    def ipaddr_client_hostname(self):
        return self.ipaddr_client_appname + "." + self.domain


CONFIG = Config()
