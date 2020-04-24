import os
import shutil
import subprocess

from teds import utils

tmp = os.environ.get("TEST_TMP_ROOT", '/tmp')
clone_into = f'{tmp}/helm-ted-ci/raw'
copy_into = f'{tmp}/helm-ted-ci/chart'
local_repo = f'{utils.project_root()}/test/sim_chart_repo'
overrides_dir = f'{utils.project_root()}/test/overrides'

def set_env(**kwargs):
  for key, value in kwargs.items():
    os.environ[key.upper()] = value


def git_init_local_repo():
  here = utils.exec_cmd("pwd")
  cmd = f"cd {local_repo}; " \
        f"git init; " \
        f"git add . -A; " \
        f"git commit -m 't'; " \
        f"cd {here}"
  subprocess.check_output(cmd, shell=True)


def clean_up():
  if os.path.exists(copy_into):
    shutil.rmtree(copy_into)
  if os.path.exists(clone_into):
    shutil.rmtree(clone_into)
  if os.path.exists(f'{local_repo}/.git'):
    shutil.rmtree(f'{local_repo}/.git')
  set_env(
    clone_into_dir='',
    repo_subpath='',
    working_dir='',
    repo_name='',
  )
