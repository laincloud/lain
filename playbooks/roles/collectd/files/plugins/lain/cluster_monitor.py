#!/usr/bin/python
# -*- coding:utf-8 -*-


import os
import time
import socket
import psutil
import subprocess
import argparse
import sys
import requests
from plugin import Plugin, GraphiteData
from procutils import get_etcd_value, convert_to_byte


class ClusterPlugin(Plugin):

    _result = []
    _step = 0
    _endpoint = socket.gethostname()

    def __init__(self, step, swarm_manager_port, docker_port, ceph_fuse):
        self._swarm_manager_port = swarm_manager_port
        self._docker_port = docker_port
        self._step = step
        self._ceph_fuse = ceph_fuse

    def prepare_data(self):
        self._result = []
        self._get_cali_veth_stat()
        self._get_mfs_stat()
        self._get_ceph_stat()
        self._get_etcd_stat()
        self._get_swarm_stat()
        self._get_docker_devicemapper_stat()
        return self._result

    def _get_cali_veth_stat(self):
        '''
        Check the status of all network interfaces.
        Value is 1 if any one of them is DOWN
        '''
        cali_veth_up = 0
        cali_veth_down = 0
        cali_veth_total = 0
        tmp_veth_up = 0
        tmp_veth_down = 0
        tmp_veth_total = 0
        for name, stat in psutil.net_if_stats().iteritems():
            if name.startswith('cali'):
                cali_veth_total += 1
                if stat.isup:
                    cali_veth_up += 1
                else:
                    cali_veth_down += 1
            elif name.startswith('tmp'):
                tmp_veth_total += 1
                if stat.isup:
                    tmp_veth_up += 1
                else:
                    tmp_veth_down += 1
        self._result.append(
            GraphiteData("lain.cluster.calico.veth.cali.up",
                         self._endpoint, cali_veth_up, self._step, "val"))
        self._result.append(
            GraphiteData("lain.cluster.calico.veth.cali.down",
                         self._endpoint, cali_veth_down, self._step, "val"))
        self._result.append(
            GraphiteData("lain.cluster.calico.veth.cali.total",
                         self._endpoint, cali_veth_total, self._step, "val"))
        self._result.append(
            GraphiteData("lain.cluster.calico.veth.tmp.up",
                         self._endpoint, tmp_veth_up, self._step, "val"))
        self._result.append(
            GraphiteData("lain.cluster.calico.veth.tmp.down",
                         self._endpoint, tmp_veth_down, self._step, "val"))
        self._result.append(
            GraphiteData("lain.cluster.calico.veth.tmp.total",
                         self._endpoint, tmp_veth_total, self._step, "val"))

    def _get_mfs_stat(self):
        '''
        Get the mfs status
        '''
        is_mounted = 1 if os.path.ismount("/mfs") else 0
        self._result.append(
            GraphiteData("lain.cluster.mfs.mounted", self._endpoint,
                         is_mounted, self._step, "status"))

    def _get_ceph_stat(self):
        '''
        Get the mfs status
        '''
        is_mounted = 1 if os.path.ismount(self._ceph_fuse) else 0
        self._result.append(
            GraphiteData("lain.cluster.cephfuse.mounted", self._endpoint,
                         is_mounted, self._step, "status"))

    def _get_etcd_stat(self):
        is_alive = 0
        try:
            out = subprocess.check_output("etcdctl cluster-health", shell=True)
        except subprocess.CalledProcessError:
            pass

        if out.find("unhealthy") == -1:  # All swarm-agent is healthy
            is_alive = 1
        self._result.append(
            GraphiteData("lain.cluster.etcd.alive", self._endpoint,
                         is_alive, self._step, "status"))

    def _get_swarm_stat(self):
        leader = get_etcd_value("/lain/swarm/docker/swarm/leader")
        cmd = ["timeout", "3", "docker", "-H",
               "swarm.lain:%d" % self._swarm_manager_port, "version"]
        is_healthy = 0
        is_alive = 0
        has_leader = 0

        if leader != "":
            has_leader = 1

        with open("/dev/null", "w") as f:
            if subprocess.call(cmd, stdout=f) == 0:
                is_alive = 1

            cmd[5] = "info"
            if subprocess.call(cmd, stdout=f) == 0:
                is_healthy = 1

        self._result.append(
            GraphiteData("lain.cluster.swarm.alive", self._endpoint,
                         is_alive, self._step, "status"))
        self._result.append(
            GraphiteData("lain.cluster.swarm.health", self._endpoint,
                         is_healthy, self._step, "status"))
        self._result.append(
            GraphiteData("lain.cluster.swarm.leaderkey", self._endpoint,
                         has_leader, self._step, "status"))

    def _get_docker_devicemapper_stat(self):
        data_percent = 0
        meta_percent = 0
        try:
            resp = requests.get(
                "http://docker.lain:%s/info" % self._docker_port,
                timeout=5)
            data = resp.json()
            driver_status = data["DriverStatus"]
            data_used = 0
            data_total = 0
            meta_used = 0
            meta_total = 0

            for stat in driver_status:
                if stat[0] == "Data Space Total":
                    data_total = self._get_size_byte(stat[1])
                elif stat[0] == "Data Space Used":
                    data_used = self._get_size_byte(stat[1])
                elif stat[0] == "Metadata Space Total":
                    meta_total = self._get_size_byte(stat[1])
                elif stat[0] == "Metadata Space Used":
                    meta_used = self._get_size_byte(stat[1])

            if data_total != 0:
                data_percent = "%.2f" % (data_used / data_total)
            if meta_total != 0:
                meta_percent = "%.2f" % (meta_used / meta_total)
        except Exception:
            pass

        self._result.append(
            GraphiteData("lain.cluster.docker.devicemapper.data.used",
                         self._endpoint, data_percent, self._step, "percent"))
        self._result.append(
            GraphiteData("lain.cluster.docker.devicemapper.metadata.used",
                         self._endpoint, meta_percent, self._step, "percent"))

    def _get_size_byte(self, size_str):
        parts = size_str.split(" ")
        if len(parts) == 2:
            return convert_to_byte(parts[0], parts[1])
        else:
            return 0

if __name__ == "__main__":
    step = 60
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument("--swarm-manager-port", help="Swarm manager port",
                        default=2376, type=int)
    parser.add_argument("--docker-port", help="Dockerd port",
                        default=2375, type=int)
    parser.add_argument("--ceph-fuse", help="Ceph fuse mountpoint",
                        default="/data/lain/cloud-volumes", type=str)

    args = parser.parse_args()
    cluster_plugin = ClusterPlugin(step, args.swarm_manager_port, args.docker_port, args.ceph_fuse)
    if args.verbose:
        cluster_plugin.verbose()
    else:
        while True:
            cluster_plugin.report()
            sys.stdout.flush()
            time.sleep(step)
