# -*- coding: utf-8 -*-

import collectd
import requests
import time


class Plugin(object):
    DOCKER_URL_PREFIX = "http://docker.lain:2375"
    READ_INTERVAL = 600  # 600 seconds
    TIMEOUT = 6  # 6 seconds
    NAME = "lain.cluster.node"

    def init(self):
        collectd.info("node_monitor plugin has been initialized.")

    def __get(self, location, params=None, **kwargs):
        url = "{}{}".format(self.DOCKER_URL_PREFIX, location)
        return requests.get(url, params, timeout=self.TIMEOUT, **kwargs).json()

    def __get_all_container_ids(self):
        containers = self.__get("/containers/json")
        return [c["Id"] for c in containers]

    def read_docker_reserved_cpu_cores(self, container_ids):
        '''
        Unit: CPU Cores
        '''
        docker_reserved_cpu_cores = 0
        for container_id in container_ids:
            inspect_info = self.__get("/containers/{}/json".format(
                container_id))
            docker_reserved_cpu_cores += self.__calculate_docker_reserved_cpu_cores(
                inspect_info)

        metric = collectd.Values()
        metric.plugin = self.NAME
        metric.plugin_instance = "docker_reserved_cpu_cores"
        metric.type = "val"
        metric.values = [docker_reserved_cpu_cores]
        metric.dispatch()

    def __calculate_docker_reserved_cpu_cores(self, inspect_info):
        cpu_quota = inspect_info["HostConfig"]["CpuQuota"]
        cpu_period = inspect_info["HostConfig"]["CpuPeriod"]
        if cpu_quota > 0 and cpu_period > 0:
            return (float(cpu_quota) / cpu_period)

        return 0

    def read_docker_used_cpu_cores(self, container_ids):
        '''
        Unit: CPU Cores
        '''
        docekr_used_cpu_cores = 0
        for container_id in container_ids:
            stats = self.__get("/containers/{}/stats?stream=false".format(
                container_id))
            docekr_used_cpu_cores += self.__calculate_docker_used_cpu_cores(
                stats)
        metric = collectd.Values()
        metric.plugin = self.NAME
        metric.plugin_instance = "docker_used_cpu_cores"
        metric.type = "val"
        metric.values = [docekr_used_cpu_cores]
        metric.dispatch()

    def __calculate_docker_used_cpu_cores(self, stats):
        '''
        Unit: CPU Cores
        '''
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats[
            "precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats[
            "precpu_stats"]["system_cpu_usage"]
        if cpu_delta > 0 and system_delta > 0:
            return (float(cpu_delta) / system_delta
                    ) * len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"])

        return 0

    def read(self):
        try:
            container_ids = self.__get_all_container_ids()
            self.read_docker_used_cpu_cores(container_ids)
            time.sleep(10)
            self.read_docker_reserved_cpu_cores(container_ids)
        except Exception as e:
            collectd.error("read() failed, exception: {}".format(e))

    def shutdown(self):
        collectd.info("node_monitor plugin has been shutdown.")


if __name__ != "__main__":
    node_monitor = Plugin()
    collectd.register_init(node_monitor.init)
    collectd.register_read(node_monitor.read, node_monitor.READ_INTERVAL)
    collectd.register_shutdown(node_monitor.shutdown)
