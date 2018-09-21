#!/usr/bin/env python

from subprocess import check_output, call, CalledProcessError, STDOUT
from collections import OrderedDict


def deduplicate(seq):
    return list(OrderedDict.fromkeys(seq))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            images=dict(required=True, type='list'),
            redundancy=dict(required=True, type='int'),
        )
    )
    images = module.params['images']
    redundancy = module.params['redundancy']
    filter_key_list = ["rebellion", "swarm"]

    tag_type = ['release', 'meta']
    save_image_set = set()
    try:
        for image in images:
            for tag in tag_type:
                save_image_set = save_image_set | get_save_images(image, tag, redundancy, filter_key_list=filter_key_list)
        module.exit_json(changed=remove_extra_images(save_image_set))
    except Exception as e:
        module.fail_json(msg=str(e))


def get_save_images(image, tag_type, redundancy, filter_key_list=None):
    if filter_key_list is None:
        filter_key_list = []

    try:
        docker_images_output = check_output(['docker', 'images', image], stderr=STDOUT)
    except CalledProcessError as e:
        raise Exception('Error getting Docker image list: {}'.format(e.stdout))

    image_list = docker_images_output.splitlines()
    image_list.pop(0)  # Remove table header

    image_names = []

    # 0:REPOSITORY, 1:TAG, 2:IMAGE ID, 3:CREATED, 4:VIRTUAL SIZE
    for row in image_list:
        cols = [i.strip() for i in row.split('  ') if i]  # Columns are seperated by at least two spaces
        image_name = '{}:{}'.format(cols[0], cols[1])
        if cols[1].startswith(tag_type):
            image_names.append(image_name)
        # keep those images with tag not start with tag_type
        for key in filter_key_list:
            if key in image_name:
                image_names.append(image_name)

    image_names = deduplicate(image_names)

    return set(image_names[-redundancy:])


def remove_extra_images(save_image_set):
    changed = False

    try:
        docker_images_output = check_output(['docker', 'images'], stderr=STDOUT)
    except CalledProcessError as e:
        raise Exception('Error getting Docker image list: {}'.format(e.stdout))

    image_list = deduplicate(docker_images_output.splitlines())
    image_list.pop(0)  # Remove table header

    # 0:REPOSITORY, 1:TAG, 2:IMAGE ID, 3:CREATED, 4:VIRTUAL SIZE
    for row in image_list:
        cols = [i.strip() for i in row.split('  ') if i]  # Columns are seperated by at least two spaces
        image_name = '{}:{}'.format(cols[0], cols[1])
        if image_name not in save_image_set:
            changed = (call(['docker', 'rmi', image_name]) == 0) or changed
    return changed


from ansible.module_utils.basic import *
main()
