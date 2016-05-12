import psutil
import subprocess


SIZE_KB = 1 << 10
SIZE_MB = 1 << 20
SIZE_GB = 1 << 30
SIZE_TB = 1 << 40

SCALE_MAP = {
    "KB": SIZE_KB,
    "MB": SIZE_MB,
    "GB": SIZE_GB,
    "TB": SIZE_TB,
    "B":  1,
}


def get_proc(proc_name):
    '''
    Get the process info by name
    '''
    for p in psutil.process_iter():
        if p.name() == proc_name:
            return p
    return None


def get_etcd_value(key):
    out = ""
    try:
        out = subprocess.check_output(['etcdctl', 'get', key])
    except subprocess.CalledProcessError:
        pass
    return out.strip()


def convert_to_byte(value, scale):
    if scale in SCALE_MAP:
        return float(value) * SCALE_MAP[scale]
    else:
        return 0
