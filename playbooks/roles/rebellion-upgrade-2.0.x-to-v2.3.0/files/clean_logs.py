#!/usr/bin/env python
import os
import requests
import json

def clean_content(file_path):
    print "Cleaning %s..." % file_path
    open(file_path, 'w').close()

def clean_webrouter():
    webrouter_dir1 = '/data/lain/volumes/webrouter/webrouter.worker.worker/1/var/log/nginx'
    webrouter_dir2 = '/data/lain/volumes/webrouter/webrouter.worker.worker/2/var/log/nginx'
    for root, dirs, files in os.walk(webrouter_dir1, True):
        for name in files:
            clean_content(os.path.join(root, name))
    for root, dirs, files in os.walk(webrouter_dir2, True):
        for name in files:
            clean_content(os.path.join(root, name))

def clean_syslog():
    clean_content("/var/log/messages")

def clean_applog():
    resp = requests.get('http://lainlet.lain:9001/v2/rebellion/localprocs')
    respData = resp.json()
    for proc_name, proc_info in respData.iteritems():
        parts = proc_name.split(".")
        if len(parts) < 3:
            continue
        app_name = parts[0]
        if len(proc_info["PodInfos"]) > 0:
            container_info = proc_info["PodInfos"][0]
            annotations = json.loads(container_info["Annotation"])
            if "logs" in annotations:
                for log_file in annotations["logs"]:
                    clean_content(os.path.join("/data/lain/volumes", app_name, proc_name, str(container_info["InstanceNo"]), "lain/logs", log_file))

if __name__ == "__main__":
    clean_webrouter()
    clean_syslog()
    clean_applog()