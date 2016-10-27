#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import docker
import json
import os
import time
import sys
import argparse

CONFIGS = {}


class Plugin:
    @classmethod
    def create_record(cls, metric, value, lain_info, metric_type="GAUGE"):
        interval = CONFIGS['interval']
        host = lain_info["host"]
        plugin = lain_info["plugin"]
        plugin = plugin.replace('-', '_')
        plugin_instance = lain_info["plugin_instance"]
        type, type_instance = metric.split('.')
        print 'PUTVAL "%s/%s-%s/%s-%s" interval=%s N:%s' % (host, plugin, plugin_instance,
                                                            type, type_instance, interval, value)


class CpuStats(Plugin):
    @classmethod
    def get(cls, stats, lain_info):
        # docker cpu stats is nanoseconds, plus 100 for percent, *100/1e9 = /1e7
        cls.create_record("cpu.total", int(int(stats["cpu_stats"]["cpu_usage"]["total_usage"])/1e7), lain_info)
        cls.create_record("cpu.user", int(int(stats["cpu_stats"]["cpu_usage"]["usage_in_usermode"])/1e7), lain_info)
        cls.create_record("cpu.kernel", int(int(stats["cpu_stats"]["cpu_usage"]["usage_in_kernelmode"])/1e7), lain_info)


class MemoryStats(Plugin):
    @classmethod
    def get(cls, stats, lain_info):
        usage = stats["memory_stats"]["usage"]
        cls.create_record("memory.usage", usage, lain_info)

        stat_list = stats["memory_stats"]["stats"]
        if not stat_list:
            return
        for stat in stat_list:
            if stat.startswith("total_"):
                metric = "memory.%s" % (stat[6:])
                value = stat_list[stat]
                cls.create_record(metric, value, lain_info)


"""
"blkio_stats": {
    "io_merged_recursive": [],
    "io_queue_recursive": [],
    "io_service_bytes_recursive": [],
    "io_service_time_recursive": [],
    "io_serviced_recursive": [],
    "io_time_recursive": [],
    "io_wait_time_recursive": [],
    "sectors_recursive": []
}
"""
class BlkioStats(Plugin):
    @classmethod
    def get(cls, stats, lain_info):
        for stat, value in stats["blkio_stats"].iteritems():
            for item in value:
                cls.create_record("blkio.%s-%s" % (stat, item['op']), item['value'], lain_info, "COUNTER")


"""
"networks": {
    "rx_bytes": 0,
    "rx_dropped": 0,
    "rx_errors": 0,
    "rx_packets": 0,
    "tx_bytes": 0,
    "tx_dropped": 0,
    "tx_errors": 0,
    "tx_packets": 0
},
"""
class NetworkStats(Plugin):
    @classmethod
    def get(cls, stats, lain_info):
        if "networks" not in stats:
            return
        for interface in stats["networks"]:
            for stat in stats["networks"][interface]:
                cls.create_record("net.%s-%s" % (interface, stat), stats["networks"][interface][stat], lain_info, "COUNTER")


class Docker:
    BASE_URL = "unix://var/run/docker.sock"
    client = docker.Client(base_url=BASE_URL)

    @classmethod
    def get_stats(cls, container_id):
        st = cls.client.stats(container_id, decode=True)
        return st.next()

    @classmethod
    def get_inspect_env(cls, container_id):
        env_dict = {}
        envlist = cls.client.inspect_container(container_id)["Config"]["Env"]
        if envlist:
            for env in envlist:
                try:
                    key, value = env.strip().split("=")
                    env_dict[key] = value
                except ValueError:
                    continue
        return env_dict

    @classmethod
    def get_all_running_containers(cls):
        result = []
        for container in cls.client.containers():
            if container["Status"].startswith("Up"):
                result.append(container)
        return result



class Lainlet(object):

    def __init__(self, url, hostname):
        self.url = url
        self.hostname = hostname

    def get_containers(self):
        # app: DOMAIN.app.APPNAME.proc.PROCNAME.instance.NO.
        url = "%s/v2/containers?nodename=%s" % (self.url, self.hostname)
        r = urllib.urlopen(url)
        containers = json.loads(r.read())
        info = {}
        for key, val in containers.iteritems():
            name = key.partition('/')[-1]
            podname = val['proc']
            parts = podname.split('.')
            info[name] = {}
            info[name]['app_name'] = val['app']
            info[name]['node_name'] = val['nodename']
            info[name]['instance_no'] = val['instanceNo']
            info[name]['proc_name'] = parts[-1]
            info[name]['proc_type'] = parts[-2]
        return info

    def get_depends(self):
        # portal: DOMAIN.app.[SERVICE|RESOURCE].portal.PORTALNAME.APPNAME.NODENAME.(instance.NO.)
        url = "%s/v2/depends" % (self.url)
        r = urllib.urlopen(url)
        depends = json.loads(r.read())
        info = {}
        for key, val in depends.iteritems():
            for host, hval in val.iteritems():
                for app, aval in hval.iteritems():
                    service_name, _, _ = key.rsplit('.', 2)
                    service_name = service_name.replace('.', '_')  # for resource
                    name = "%s-%s-%s" % (key, host, app)
                    info[name] = {}
                    info[name]['app_name'] = app
                    info[name]['node_name'] = host
                    info[name]['portal_name'] = json.loads(aval['Annotation'])['service_name']
                    info[name]['service_name'] = service_name
                    info[name]['proc_name'] = None
                    info[name]['proc_type'] = None
        return info

    @classmethod
    def get_info(cls, containers, depends, container_id, container_name):
        info = {}
        if container_id in containers:
            info["plugin"] = "app.%s.proc.%s" % (
                containers[container_id]["app_name"],
                containers[container_id]["proc_name"],
            )
            info["plugin_instance"] = containers[container_id]["instance_no"]
            info["host"] = CONFIGS['domain']
            return info
        name = container_name.rpartition('.')[0]
        if name in depends:
            info["plugin"] = "app.%s.portal.%s.%s.%s" % (
                depends[name]["service_name"],
                depends[name]["portal_name"],
                depends[name]["app_name"],
                depends[name]["node_name"],
            )
            info["plugin_instance"] = "0"
            info["host"] = CONFIGS['domain']
            return info
        # non-lain app: calico/swarm
        info["plugin"] = "docker.%s" % container_name.replace('.', '_')
        info["plugin_instance"] = "0"
        info["host"] = CONFIGS["hostname"]
        return info


CONFIGS['hostname'] = os.uname()[1]
CONFIGS['interval'] = 60

CLASSES = [CpuStats, MemoryStats, NetworkStats, BlkioStats]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lainlet-endpoint", help="lainlet endpoint",
                default="http://lainlet.lain:9001", type=str)
    parser.add_argument("--domain", help="lain domain",
                default="lain.local", type=str)
    args = parser.parse_args()
    CONFIGS['domain'] = args.domain.replace('.', '_')
    lainlet = Lainlet(args.lainlet_endpoint, CONFIGS['hostname'])

    while True:
        containers = lainlet.get_containers()
        depends = lainlet.get_depends()

        for container in Docker.get_all_running_containers():
            # eg: mysql-service.portal.portal-mysql-master-xyz-101-hedwig.v0-i0-d0
            # eg: webrouter.worker.worker.v8-i1-d0
            # eg: resource.hello-server.perf.worker.hello.v0-i2-d0
            container_name = container["Names"][0].strip('/')
            container_id = container["Id"]
            stats = Docker.get_stats(container_id)
            lain_info = lainlet.get_info(containers, depends, container_id, container_name)

            for klass in CLASSES:
                klass.get(stats, lain_info)
        sys.stdout.flush()
        time.sleep(CONFIGS['interval'])
