# -*- coding: utf-8 -*-

import collectd
import time
import requests


class Plugin(object):
    DOCKER_INFO_URL = "http://docker.lain:2375/info"
    READ_INTERVAL = 60  # 60 seconds
    TIMEOUT = 5  # 5 seconds

    def init(self):
        collectd.info("docker_daemon_monitor plugin has been initialized.")

    def read(self):
        metric = collectd.Values()
        metric.plugin = "lain.cluster.docker_daemon"
        metric.plugin_instance = "docker_info_time"
        metric.type = "val"
        start_at = time.time()
        requests.get(self.DOCKER_INFO_URL, timeout=self.TIMEOUT)
        docker_info_time = time.time() - start_at
        metric.values = [docker_info_time]
        metric.dispatch()

    def shutdown(self):
        collectd.info("docker_daemon_monitor plugin has been shutdown.")

    def __timeout_handler(self, signum, frame):
        raise IOError("docker hangs")


docker_daemon = Plugin()

if __name__ != "__main__":
    collectd.register_init(docker_daemon.init)
    collectd.register_read(docker_daemon.read, docker_daemon.READ_INTERVAL)
    collectd.register_shutdown(docker_daemon.shutdown)
