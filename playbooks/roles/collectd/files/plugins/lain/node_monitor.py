# -*- coding: utf-8 -*-

import collectd
import requests


class Plugin(object):
    DOCKER_URL_PREFIX = "http://docker.lain:2375"
    READ_INTERVAL = 300  # 300 seconds
    TIMEOUT = 3  # 3 seconds
    NAME = "lain.cluster.node"

    def init(self):
        collectd.info("node_monitor plugin has been initialized.")

    def read_docker_used_cpu_cores(self):
        '''
        Unit: CPU Cores
        '''
        try:
            containers = requests.get(
                "{}/containers/json".format(self.DOCKER_URL_PREFIX),
                timeout=self.TIMEOUT).json()
            docekr_used_cpu_cores = 0
            for container in containers:
                stats = requests.get(
                    "{}/containers/{}/stats?stream=false".format(
                        self.DOCKER_URL_PREFIX, container["Id"]),
                    timeout=self.TIMEOUT).json()
                docekr_used_cpu_cores += self.__calculate_cpu_cores(stats)
            metric = collectd.Values()
            metric.plugin = self.NAME
            metric.plugin_instance = "docker_used_cpu_cores"
            metric.type = "val"
            metric.values = [docekr_used_cpu_cores]
            metric.dispatch()
        except Exception as e:
            collectd.error("read failed, exception: {}".format(e))

    def read(self):
        self.read_docker_used_cpu_cores()

    def shutdown(self):
        collectd.info("node_monitor plugin has been shutdown.")

    def __calculate_cpu_cores(self, stats):
        '''
        Unit: CPU Cores
        '''
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats[
            "precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats[
            "precpu_stats"]["system_cpu_usage"]
        if cpu_delta > 0 and system_delta > 0:
            return (
                float(cpu_delta) / system_delta
            ) * len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"])

        return 0


node_monitor = Plugin()

if __name__ != "__main__":
    collectd.register_init(node_monitor.init)
    collectd.register_read(node_monitor.read, node_monitor.READ_INTERVAL)
    collectd.register_shutdown(node_monitor.shutdown)
