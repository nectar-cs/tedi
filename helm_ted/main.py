import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from typing import List, Dict


chart_clone_dir = lambda: os.environ.get('CHART_CLONE_DIR')
desired_subpath = lambda: os.environ.get('CHART_SUB_PATH', '')
chart_path = lambda: os.environ.get('CHART_DIR')
overrides_path = lambda: f"{chart_path}/overrides.yaml"
values_path = lambda: f"{chart_path}/values.yaml"
repo_name = lambda: os.environ.get('CHART_REPO')


def exec_cmd(cmd):
  raw = subprocess.check_output(cmd, shell=True)
  as_str = raw.decode("utf-8")
  return as_str[:-1]


def deep_merge(source, destination):
  for key, value in source.items():
    if isinstance(value, dict):
      node = destination.setdefault(key, {})
      deep_merge(value, node)
    else:
      destination[key] = value
    return destination


def clone_chart_repo_cmd():
  return f"git clone {repo_name()} {chart_clone_dir()}"


def cp_repo_to_dir_cmd():
  _actual_subpath = f"{desired_subpath()}/" if desired_subpath() else ''
  copy_from = f"{chart_clone_dir()}/{_actual_subpath}."
  copy_to = chart_path()
  return f"rsync -r {copy_from} {copy_to}"



def init_helm():
  exec_cmd(clone_chart_repo_cmd())
  exec_cmd(cp_repo_to_dir_cmd())


def res_matches(res, identifier) -> bool:
  if res['kind'] == identifier['kind']:
    if res['metadata']['name'] == identifier['name']:
      return True
  return False


def interpolate():
  f_paths = " -f ".join([values_path(), overrides_path()])
  command = f"helm template {cloned_helm_path()} -f {f_paths}"
  output = subprocess.check_output(command, shell=True)
  output = output.decode('utf-8').replace('RELEASE-NAME-', '')
  res_iterator = yaml.load_all(output, yaml.FullLoader)
  return [res for res in res_iterator]


def write_res(res_defs: List[Dict]):
  as_yaml = yaml.dump_all(res_defs)
  print(as_yaml)

def read_override_values():
  path = os.environ.get(
    'NECTAR_VALUES_PATH',
    mk_path('/dummy_config')
  )
  return json.loads(open(path, 'r').read())


def create_overrides_yaml():
  file = open(overrides_path(), "w")
  file.write(yaml.dump(read_override_values()))
  file.close()


def parse_ids(ser_ids):
  to_dict = lambda x: dict(kind=x[0], name=x[1])
  return [to_dict(pair.split(':')) for pair in ser_ids]


def main():
  if len(sys.argv) < 1:
    print("Need 1 arg")
  elif sys.argv[1] == 'init':
    init_helm()
  elif sys.argv[1] == 'interpolate':
    print(interpolate())


if __name__ == '__main__':
  main()
  sys.exit(0)
