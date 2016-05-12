#!/usr/bin/env python

"""Draw a dependency graph for all the roles."""

import sys
import os
import yaml

CWD = os.path.abspath(os.path.dirname(__file__))
ENTRY = 'bootstrap'
SEEN = set()
HIDE_SEEN = True


def get_dep_roles(role_name):
    meta_paths = [
        os.path.join(CWD, 'roles', role_name, 'meta', main_yaml)
        for main_yaml in ['main.yaml', 'main.yml']
    ]
    meta_path = next((mp for mp in meta_paths if os.path.exists(mp)), None)
    if not meta_path:
        return None
    meta = yaml.safe_load(open(meta_path).read())
    deps = meta.get('dependencies', [])
    dep_roles = [
        d if isinstance(d, str)
        else d['role']
        for d in deps
    ]
    return dep_roles


def draw_dep_roles(dep_roles, level, hide_seen=HIDE_SEEN):
    for dep_role in dep_roles:
        if hide_seen and dep_role in SEEN:
            continue
        print('{}- {}'.format('    ' * (level + 1), dep_role))
        SEEN.add(dep_role)
        next_dep_roles = get_dep_roles(dep_role)
        if not next_dep_roles:
            continue
        draw_dep_roles(next_dep_roles, level + 1)


def main(entry=ENTRY):
    print(ENTRY)
    dep_roles = get_dep_roles(entry)
    draw_dep_roles(dep_roles, 0)


if __name__ == '__main__':
    sys.exit(main())
