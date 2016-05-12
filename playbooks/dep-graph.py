#!/usr/bin/env python

"""Draw a dependency graph for all the roles."""

import sys
import os
import yaml

here = os.path.abspath(os.path.dirname(__file__))


def main():
    roles = os.listdir(os.path.join(here, 'roles'))
    print("digraph G {")

    for role in roles:
        meta_paths = [os.path.join(here, 'roles', role, 'meta', x)
                      for x in ['main.yaml', 'main.yml']]
        for meta_path in meta_paths:
            if os.path.exists(meta_path):
                meta = yaml.safe_load(open(meta_path).read())
                for dependency in meta.get('dependencies', []):
                    dep = dependency if isinstance(dependency, str) else dependency['role']
                    print('"{}" -> "{}"'.format(role, dep))
                break
    print("}")


if __name__ == '__main__':
    sys.exit(main())
