import os
import shutil
import subprocess
import unittest

import yaml
from dotenv import load_dotenv

from helm_ted import main

load_dotenv()

clone_into = '/tmp/helm-ted-ci/raw'
copy_into = '/tmp/helm-ted-ci/chart'
local_repo = 'sim_chart_repo'
overrides_dir = 'overrides'

full_path = os.path.realpath(__file__)
print("FIRST " + full_path + "\n")

print("This file directory and name")
path, filename = os.path.split(full_path)
print(path + ' --> ' + filename + "\n")

def set_env(**kwargs):
  for key, value in kwargs.items():
    os.environ[key.upper()] = value


def git_init_local_repo():
  cmd = f"cd {local_repo}; " \
        f"git init; " \
        f"git add . -A; " \
        f"git commit -m 't'; " \
        f"cd .."
  subprocess.check_output(cmd, shell=True)


def clean_up():
  if os.path.exists(copy_into):
    shutil.rmtree(copy_into)
  if os.path.exists(clone_into):
    shutil.rmtree(clone_into)
  if os.path.exists(f'{local_repo}/.git'):
    shutil.rmtree(f'{local_repo}/.git')
  set_env(
    chart_clone_dir='',
    chart_sub_path='',
    chart_dir='',
    chart_repo='',
  )


def setup_interp(file):
  set_env(
    chart_repo=local_repo,
    chart_clone_dir=clone_into,
    chart_dir=copy_into,
    overrides_path=f'{overrides_dir}/{file}.yaml'
  )
  git_init_local_repo()
  main.init_helm()
  return list(yaml.load_all(main.interpolate(), Loader=yaml.FullLoader))[0]


class TestMain(unittest.TestCase):

  def setUp(self) -> None:
    clean_up()

  def tearDown(self) -> None:
    clean_up()

  def test_exec_cmd(self):
    self.assertEqual(main.exec_cmd("echo foo"), "foo")

  def test_clone_chart_repo_cmd(self):
    set_env(
      chart_repo='http://a-host.my/repo',
      chart_clone_dir='/path'
    )
    actual = main.clone_chart_repo_cmd()
    self.assertEqual(actual, "git clone http://a-host.my/repo /path")

  def test_cp_repo_to_dir_cmd_when_subpath(self):
    set_env(
      chart_clone_dir='/from/path',
      chart_dir='/chart',
      chart_sub_path='inner/repo'
    )
    actual = main.cp_repo_to_dir_cmd()
    self.assertEqual(actual, "rsync -r /from/path/inner/repo/. /chart")

  def test_cp_repo_to_dir_cmd_no_subpath(self):
    set_env(
      chart_clone_dir='/from/path',
      chart_dir='/chart',
    )
    actual = main.cp_repo_to_dir_cmd()
    self.assertEqual(actual, "rsync -r /from/path/. /chart")

  def test_init_helm(self):
    self.assertFalse(os.path.exists(clone_into))
    set_env(
      chart_repo=local_repo,
      chart_clone_dir=clone_into,
      chart_dir=copy_into,
    )
    git_init_local_repo()
    main.init_helm()
    self.assertTrue(os.path.exists(clone_into))
    self.assertGreater(len(os.listdir(clone_into)), 1)

  def test_interpolate_without_override(self):
    svc = setup_interp('no_change')
    actual = svc['spec']['ports'][0]['port']
    self.assertEqual(actual, 9000)

  def test_interpolate_with_override(self):
    svc = setup_interp('plus_one')
    actual = svc['spec']['ports'][0]['port']
    self.assertEqual(actual, 9001)
