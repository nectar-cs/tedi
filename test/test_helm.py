import os
import unittest

import yaml
from dotenv import load_dotenv

from teds import utils, helm
from test import helper

load_dotenv()

local_repo_src = f'{utils.project_root()}/test/sim_helm_repo'

def setup_interp(file):
  overrides_path = f'{helper.overrides_dir}/{file}.yaml' if file else ''
  helper.set_env(
    repo_name=helper.local_repo,
    clone_into_dir=helper.clone_into,
    working_dir=helper.copy_into,
    overrides_path=overrides_path
  )
  helper.git_init_local_repo(local_repo_src)
  helm.init()
  return list(yaml.load_all(helm.interpolate(), Loader=yaml.FullLoader))[0]


class TestHelm(unittest.TestCase):

  def setUp(self) -> None:
    helper.clean_up()

  def tearDown(self) -> None:
    helper.clean_up()

  def test_init(self):
    self.assertFalse(os.path.exists(helper.clone_into))
    helper.set_env(
      repo_name=helper.local_repo,
      clone_into_dir=helper.clone_into,
      working_dir=helper.copy_into,
    )
    helper.git_init_local_repo(local_repo_src)
    helm.init()
    self.assertTrue(os.path.exists(helper.clone_into))
    self.assertGreater(len(os.listdir(helper.clone_into)), 1)


  def test_interpolate_without_override(self):
    svc = setup_interp(None)
    actual = svc['spec']['ports'][0]['port']
    self.assertEqual(actual, 9000)

  def test_interpolate_with_override(self):
    svc = setup_interp('plus_one')
    actual = svc['spec']['ports'][0]['port']
    self.assertEqual(actual, 9001)
