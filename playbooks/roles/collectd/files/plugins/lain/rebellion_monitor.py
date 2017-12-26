# -*- coding: utf-8 -*-

import collectd
import requests


class Plugin(object):
    DOCKER_URL_PREFIX = "http://docker.lain:2375"
    READ_INTERVAL = 60  # 60 seconds
    TIMEOUT = 6  # 6 seconds
    NAME = "lain.cluster.node"

    def init(self):
        collectd.info("rebellion_monitor plugin has been initialized.")

    def read(self):
        try:
            params = {"filters": '{"name": ["rebellion.service"]}'}
            containers = requests.get(
                "{}/containers/json".format(self.DOCKER_URL_PREFIX),
                params=params,
                timeout=self.TIMEOUT).json()
            metric = collectd.Values()
            metric.plugin = self.NAME
            metric.plugin_instance = "rebellion_service"
            metric.type = "val"
            metric.values = [len(containers)]
            metric.dispatch()
        except Exception as e:
            collectd.error(
                "rebellion_monitor.read() failed, exception: {}".format(e))

    def shutdown(self):
        collectd.info("rebellion_monitor plugin has been shutdown.")


if __name__ != "__main__":
    rebellion_monitor = Plugin()
    collectd.register_init(rebellion_monitor.init)
    collectd.register_read(rebellion_monitor.read,
                           rebellion_monitor.READ_INTERVAL)
    collectd.register_shutdown(rebellion_monitor.shutdown)
