#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import argparse
import time
import sys
import socket
from plugin import Plugin, GraphiteData
from procutils import get_etcd_value


class DeploydPlugin(Plugin):
    '''
    The monitor plugin for deployd
    '''
    _endpoint = socket.gethostname()
    _result = []

    def __init__(self, step, deployd_port):
        self._step = step
        self._deployd_port = deployd_port

    def prepare_data(self):
        self._result = []
        self._collect_deployd_debug_info()
        return self._result

    def _collect_deployd_debug_info(self):
        is_alive = 0
        try:
            domain = get_etcd_value("/lain/config/domain")
            resp = requests.get(
                "http://deployd.lain:%d/debug/vars" % self._deployd_port, timeout=1)
            if resp.status_code == 200:
                is_alive = 1
        except Exception:
            pass

        self._result.append(
            GraphiteData("lain.cluster.deployd.alive",
                         self._endpoint, is_alive, self._step, "status"))


if __name__ == "__main__":
    step = 30
    parser = argparse.ArgumentParser()
    parser.add_argument('--deployd-port', help="Deploy port", default=9003, type=int)
    args = parser.parse_args()
    deployd_plugin = DeploydPlugin(step, args.deployd_port)
    while True:
        deployd_plugin.report()
        sys.stdout.flush()
        time.sleep(step)
