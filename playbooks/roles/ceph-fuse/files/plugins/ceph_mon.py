import subprocess
import argparse
import time
import gevent
import logging
import sys
from gevent import monkey
monkey.patch_socket()

CEPH_FUSE_MOUNT_TYPE = 'ceph-fuse'
CHECK_INTERVAL_SEC = 60

log = logging.getLogger("cephmon")
log.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def check_mountpoint(mount_point):
    if mount_point.strip(' ') == '':
        return
    check_cmd = ['df', '-P', mount_point]
    check_pipe = subprocess.Popen(check_cmd, stdout=subprocess.PIPE)
    filter_pipe = subprocess.Popen(
        ["tail", "-n", "+2"], stdin=check_pipe.stdout, stdout=subprocess.PIPE)
    result_pipe = subprocess.Popen(
        ["awk", "{print $1}"], stdin=filter_pipe.stdout, stdout=subprocess.PIPE)
    filter_pipe.stdout.close()
    check_pipe.stdout.close()
    result, err = result_pipe.communicate()
    return result.strip()


def monitor(mount_point):
    while True:
        if check_mountpoint(mount_point) == CEPH_FUSE_MOUNT_TYPE:
            log.debug(mount_point + ' Successed')
        else:
            log.error(mount_point + ' Failed')
            remount(mount_point)
        time.sleep(CHECK_INTERVAL_SEC)


def start_monitors(mount_points):
    greenlets = []
    for mp in mount_points:
        greenlet = gevent.spawn(monitor, mp)
        greenlet.start()
        greenlets.append(greenlet)
    gevent.joinall(greenlets)


def fetch_mount_points(conf):
    with open(conf) as mps_file:
        lines = mps_file.readlines()
        mps = []
        for line in lines:
            mps.append(line.strip())
        return mps

def remount(mount_point):
    umount_cmd = ['umount', mount_point]
    try:
        subprocess.check_output(umount_cmd)
    except Exception as e:
        log.error(e)
        log.error('unmount '+ mount_point + ' Failed')
    mount_cmd = ['mount', mount_point]
    try:
        subprocess.check_output(mount_cmd)
        log.info('remount '+ mount_point + ' Successed')
    except Exception as e:
        log.error(e)
        log.error('mount '+ mount_point + ' Failed')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", help="Ceph fuse mountpoint",
                        default="/etc/ceph/fuse.conf", type=str)
    args = parser.parse_args()
    mount_points = fetch_mount_points(args.conf)
    start_monitors(mount_points)
