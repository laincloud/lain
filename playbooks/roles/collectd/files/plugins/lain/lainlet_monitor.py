#!/usr/bin/python
# -*- coding: utf-8 -*-

from plugin import Plugin, GraphiteData
import requests
import socket
import time
import sys
import argparse


class LainletPlugin(Plugin):
    '''
    The monitor plugin for lainlet
    '''
    _endpoint = socket.gethostname()
    _result = []

    def __init__(self, step, lainlet_port):
        self._step = step
        self._debug_url = "http://lainlet.lain:%d/debug" % (lainlet_port)

    def prepare_data(self):
        self._result = []
        self._collect_lainlet_debug_info()
        return self._result

    def _collect_lainlet_debug_info(self):
        connections = 0
        goroutines = 0
        try:
            resp = requests.get(self._debug_url, timeout=1)
            data = resp.json()
            connections = data['connections']
            goroutines = data['goroutines']
        except Exception:
            pass

        self._result.append(
            GraphiteData("lain.cluster.lainlet.goroutines",
                         self._endpoint, goroutines, self._step, "val"))
        self._result.append(
            GraphiteData("lain.cluster.lainlet.connections",
                         self._endpoint, connections, self._step, "val"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lainlet-port", help="Lainlet port",
                        default=9001, type=int)
    args = parser.parse_args()
    step = 30
    lainlet_plugin = LainletPlugin(step, args.lainlet_port)
    while True:
        lainlet_plugin.report()
        sys.stdout.flush()
        time.sleep(step)
