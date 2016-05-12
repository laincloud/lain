#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import pytest
import subprocess32 as subproc

@pytest.fixture(scope="session")
def up_node1(request):
    def fin():
        subproc.call(['sudo', 'vagrant', 'destroy', '-f', 'node1'])
    request.addfinalizer(fin)

    subproc.check_call(['sudo', 'vagrant', 'destroy', '-f', 'node1'])
    subproc.check_call(['sudo', 'vagrant', 'up', 'node1'])

@pytest.fixture(scope="session")
def up_node2(request):
    def fin():
        subproc.call(['sudo', 'vagrant', 'destroy', '-f', 'node2'])
    request.addfinalizer(fin)

    subproc.check_call(['sudo', 'vagrant', 'destroy', '-f', 'node2'])
    subproc.check_call(['sudo', 'vagrant', 'up', 'node2'])

@pytest.fixture(scope="session")
def up_node3(request):
    def fin():
        subproc.call(['sudo', 'vagrant', 'destroy', '-f', 'node3'])
    request.addfinalizer(fin)

    subproc.check_call(['sudo', 'vagrant', 'destroy', '-f', 'node3'])
    subproc.check_call(['sudo', 'vagrant', 'up', 'node3'])

@pytest.fixture(scope="session")
def bootstrap(up_node1):
    subproc.check_call(['sudo', 'vagrant', 'ssh', 'node1', '-c',
        'sudo /vagrant/bootstrap -r registry.aliyuncs.com/laincloud'])

@pytest.fixture(scope="session")
def prepare_demo_images(bootstrap):
    subproc.check_call(['sudo', 'vagrant', 'ssh', 'node1', '-c',
        'sh /vagrant/demo_images.sh'])

@pytest.fixture(scope="session")
def add_node(bootstrap, up_node2, up_node3):
    subproc.check_call(['sudo', 'vagrant', 'ssh', 'node1', '-c',
        'cd /vagrant/bootstrap_test && sudo ansible-playbook \
                -i host_vars/test-nodes distribute_ssh_key.yaml'])
    subproc.check_call(['sudo', 'vagrant', 'ssh', 'node1', '-c',
        'sudo /vagrant/add-node -q node2:192.168.77.22 node3:192.168.77.23'])
