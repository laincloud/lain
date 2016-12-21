#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import pytest
import time
import subprocess32 as subproc
from config import CONFIG
import app_ctl


@pytest.fixture(scope="session")
def up_node1():
    subproc.check_call(['sudo', 'vagrant', 'destroy', '-f', 'node1'])
    subproc.check_call(['sudo', 'vagrant', 'up', 'node1'])
    yield "node1 is ready"

    print("Destroying node1...")
    subproc.call(['sudo', 'vagrant', 'destroy', '-f', 'node1'])
    print("Node1 is destroyed.")


@pytest.fixture(scope="session")
def up_node2():
    subproc.check_call(['sudo', 'vagrant', 'destroy', '-f', 'node2'])
    subproc.check_call(['sudo', 'vagrant', 'up', 'node2'])
    yield "node2 is ready"

    print("Destroying node2...")
    subproc.call(['sudo', 'vagrant', 'destroy', '-f', 'node2'])
    print("Node2 is destroyed.")


@pytest.fixture(scope="session")
def up_node3():
    subproc.check_call(['sudo', 'vagrant', 'destroy', '-f', 'node3'])
    subproc.check_call(['sudo', 'vagrant', 'up', 'node3'])
    yield "node3 is ready"

    print("Destroying node3...")
    subproc.call(['sudo', 'vagrant', 'destroy', '-f', 'node3'])
    print("Node3 is destroyed.")


@pytest.fixture(scope="session")
def bootstrap(up_node1):
    subproc.check_call([
        'sudo', 'vagrant', 'ssh', 'node1', '-c',
        'sudo /vagrant/bootstrap -r registry.aliyuncs.com/laincloud --vip={}'.
        format(CONFIG.vip)
    ])


@pytest.fixture(scope="session")
def prepare_demo_images(bootstrap):
    subproc.check_call([
        'sudo', 'vagrant', 'ssh', 'node1', '-c',
        'sudo sh /vagrant/bootstrap_test/prepare_demo_images.sh'
    ])


@pytest.fixture(scope="session")
def reposit_ipaddr(prepare_demo_images):
    app_ctl.reposit(CONFIG.ipaddr_resource_appname)
    app_ctl.reposit(CONFIG.ipaddr_service_appname)
    app_ctl.reposit(CONFIG.ipaddr_client_appname)
    time.sleep(1)


@pytest.fixture(scope="session")
def deploy_ipaddr(reposit_ipaddr):
    app_ctl.deploy(CONFIG.ipaddr_resource_appname)
    app_ctl.deploy(CONFIG.ipaddr_service_appname)
    time.sleep(60)
    app_ctl.deploy(CONFIG.ipaddr_client_appname)
    time.sleep(30)


@pytest.fixture(scope="session")
def add_node(bootstrap, up_node2, up_node3):
    subproc.check_call([
        'sudo', 'vagrant', 'ssh', 'node1', '-c',
        'cd /vagrant/bootstrap_test && sudo ansible-playbook \
                -i host_vars/test-nodes distribute_ssh_key.yaml'
    ])
    subproc.check_call([
        'sudo', 'vagrant', 'ssh', 'node1', '-c',
        'sudo lainctl node add -p /vagrant/playbooks node2:192.168.77.22 ' +
        'node3:192.168.77.23'
    ])


@pytest.fixture(scope="session")
def scale_ipaddr_client(deploy_ipaddr, add_node):
    app_ctl.scale(CONFIG.ipaddr_client_appname, CONFIG.ipaddr_client_procname,
                  CONFIG.ipaddr_client_num_instances)
    time.sleep(30)
