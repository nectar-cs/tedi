import os
import subprocess
import sys

chart_clone_dir = lambda: os.environ.get('CHART_CLONE_DIR')
in_repo_subpath = lambda: os.environ.get('CHART_SUB_PATH', '')
chart_dir = lambda: os.environ.get('CHART_DIR')
repo_name = lambda: os.environ.get('CHART_REPO')
overrides_path = lambda: os.environ.get('OVERRIDES_PATH')
values_path = lambda: f"{chart_dir()}/values.yaml"


def exec_cmd(cmd):
  raw = subprocess.check_output(cmd, shell=True)
  as_str = raw.decode("utf-8")
  return as_str[:-1]


def clone_chart_repo_cmd():
  return f"git clone {repo_name()} {chart_clone_dir()}"


def cp_repo_to_dir_cmd():
  _actual_subpath = f"{in_repo_subpath()}/" if in_repo_subpath() else ''
  copy_from = f"{chart_clone_dir()}/{_actual_subpath}."
  copy_to = chart_dir()
  return f"rsync -r {copy_from} {copy_to}"


def init_helm():
  try:
    exec_cmd(clone_chart_repo_cmd())
    exec_cmd(cp_repo_to_dir_cmd())
    return True
  except RuntimeError:
    return False


def interpolate():
  f_paths = " -f ".join([values_path(), overrides_path()])
  command = f"helm template {chart_dir()} -f {f_paths}"
  return exec_cmd(command).replace('RELEASE-NAME-', '')


def main():
  if len(sys.argv) < 1:
    print("Need 1 arg")
  elif sys.argv[1] == 'init':
    print(init_helm(), flush=True)
  elif sys.argv[1] == 'interpolate':
    print(interpolate(), flush=True)


if __name__ == '__main__':
  main()
  sys.exit(0)
