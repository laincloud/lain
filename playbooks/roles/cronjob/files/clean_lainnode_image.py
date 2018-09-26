#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 File Name: clean_lainnode_image.py
 Author: longhui
 Created Time: 2018-09-20 11:00:50
 Descripthion: This script is used to clean the docker images on lain node, and keep several latest
"""

import sys
import re
import logging
import argparse
import pprint
from logging import handlers
from subprocess import check_output, STDOUT, CalledProcessError, call


LOGFILE = '/var/log/clean_lainnode_images.log'

log = logging.Logger(__file__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
        logging.Formatter("[%(levelname)s] %(asctime)s,%(lineno)4d, %(funcName)s : %(message)s", '%Y-%m-%d %H:%M:%S'))
fileHandler = handlers.RotatingFileHandler(LOGFILE, 'a', 10 * 1024 * 1024, 2)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(
        logging.Formatter("[%(levelname)s] %(asctime)s,%(lineno)4d, %(funcName)s : %(message)s", '%Y-%m-%d %H:%M:%S'))
log.addHandler(handler)
log.addHandler(fileHandler)

release_reg = re.compile(r'release-(\d+)-')
meta_reg = re.compile(r'meta-(\d+)-')


def get_images():
    """
    return a dict with its value as {'release':[],'meta':[]}
    :return:
    """
    all_images = {}
    cmd = "docker images --format {{.Repository}},{{.Tag}}  --no-trunc"
    try:
        output = check_output(cmd, stderr=STDOUT, shell=True)
    except CalledProcessError as e:
        log.error("Exceptions when run cmd:%s, error: %s", cmd, str(e))
        return all_images

    images_list = output.splitlines()
    for image in images_list:
        image_name, tag = image.split(',')
        all_images.setdefault(image_name, dict(release=[], meta=[]))
        res = release_reg.match(tag)
        if res:
            all_images[image_name]["release"].append('{}:{}'.format(image_name, tag))
        else:
            res = meta_reg.match(tag)
            if res:
                all_images[image_name]['meta'].append('{}:{}'.format(image_name, tag))

    return all_images


def remove_images(images_list=None, keep_num=3):
    """
    :param images_list: images list to delete
    :param keep_num: the num to keep for latest tags
    :return: None
    """
    if not images_list:
        return

    sort_images = sorted(images_list, key=lambda f: int(f.split(':')[1].split("-")[1]), reverse=True)
    delete_images = sort_images[keep_num:]

    log.debug("To delete: %s", pprint.pformat(delete_images))
    for image in delete_images:
        log.debug("Start to rm tag: %s", image)
        ret = call(['docker', 'rmi', image])
        if ret != 0:
            log.error("Remove image failed: %s", image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean docker images and keep several latest tags")

    parser.add_argument("--debug", dest="debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--keep-num", dest="keep_num", nargs='?', default=3, type=int)

    args = parser.parse_args()
    log.info(args)
    if args.debug:
        log.setLevel(logging.DEBUG)

    all_images = get_images()
    for image_name, tags in all_images.iteritems():
        log.info("Start to remove release tags in image: %s", image_name)
        remove_images(tags["release"], args.keep_num)

        log.info("Start to remove meta tags in image: %s", image_name)
        remove_images(tags['meta'], args.keep_num)
