import os
import subprocess
from pathlib import Path


clone_into_dir = lambda: os.environ.get('CLONE_INTO_DIR', '/tmp/teds/in')
working_dir = lambda: os.environ.get('WORKING_DIR', '/tmp/teds/work')
in_repo_subpath = lambda: os.environ.get('REPO_SUBPATH', '')
repo_name = lambda: os.environ.get('REPO_NAME')
overrides_path = lambda: os.environ.get('OVERRIDES_PATH')
values_path = lambda: f"{working_dir()}/values.yaml"

def project_root() -> Path:
  """Returns project root folder."""
  return Path(__file__).parent.parent


def exec_cmd(cmd):
  raw = subprocess.check_output(cmd, shell=True)
  as_str = raw.decode("utf-8")
  return as_str[:-1]


def clone_repo_cmd():
  return f"git clone {repo_name()} {clone_into_dir()}"


def cp_repo_to_dir_cmd():
  _actual_subpath = f"{in_repo_subpath()}/" if in_repo_subpath() else ''
  copy_from = f"{clone_into_dir()}/{_actual_subpath}."
  copy_to = working_dir()
  return f"rsync -r {copy_from} {copy_to}"


def init():
  try:
    exec_cmd(clone_repo_cmd())
    exec_cmd(cp_repo_to_dir_cmd())
    return True
  except RuntimeError:
    return False
