import os
import unittest
from teds import utils
from test import helper


class TestUtils(unittest.TestCase):

  def setUp(self) -> None:
    helper.clean_up()

  def tearDown(self) -> None:
    helper.clean_up()

  def test_exec_cmd(self):
    self.assertEqual(utils.exec_cmd("echo foo"), "foo")

  def test_clone_chart_repo_cmd(self):
    helper.set_env(
      repo_name='http://a-host.my/repo',
      clone_into_dir='/path'
    )
    actual = utils.clone_repo_cmd()
    self.assertEqual(actual, "git clone http://a-host.my/repo /path")

  def test_cp_repo_to_dir_cmd_when_subpath(self):
    helper.set_env(
      clone_into_dir='/from/path',
      working_dir='/chart',
      repo_subpath='inner/repo'
    )
    actual = utils.cp_repo_to_dir_cmd()
    self.assertEqual(actual, "rsync -r /from/path/inner/repo/. /chart")

  def test_cp_repo_to_dir_cmd_no_subpath(self):
    helper.set_env(
      clone_into_dir='/from/path',
      working_dir='/chart',
    )
    actual = utils.cp_repo_to_dir_cmd()
    self.assertEqual(actual, "rsync -r /from/path/. /chart")

