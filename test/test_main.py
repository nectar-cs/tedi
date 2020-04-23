import os
import shutil
import subprocess
import unittest

from dotenv import load_dotenv

from helm_ted import main

load_dotenv()

def set_env(**kwargs):
  for key, value in kwargs.items():
    os.environ[key.upper()] = value

clone_into = '/tmp/helm-ted-ci/raw'
copy_into = '/tmp/helm-ted-ci/chart'
local_repo = 'sim_chart_repo'

def git_init_local_repo():
  full_path = os.path.realpath(__file__)
  path, filename = os.path.split(full_path)
  cmd = f"cd {local_repo}; git init; git add . -A; git commit -m 't'; cd .."
  subprocess.check_output(cmd, shell=True)


class TestMain(unittest.TestCase):

  def setUp(self) -> None:
    if os.path.exists(clone_into):
      shutil.rmtree(clone_into)

  def tearDown(self) -> None:
    if os.path.exists(f'{local_repo}/.git'):
      shutil.rmtree(f'{local_repo}/.git')

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
    # self.assertTrue(os.path.exists(clone_into))
    # self.assertGreater(len(os.listdir(clone_into)), 1)

