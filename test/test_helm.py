import unittest

import yaml
from dotenv import load_dotenv

from teds import utils, helm
from test import helper

load_dotenv()

def setup_interp(file):
  helper.set_env(
    repo_name=helper.local_repo,
    clone_into_dir=helper.clone_into,
    working_dir=helper.copy_into,
    overrides_path=f'{helper.overrides_dir}/{file}.yaml'
  )
  helper.git_init_local_repo()
  utils.init()
  return list(yaml.load_all(helm.interpolate(), Loader=yaml.FullLoader))[0]


class TestMain(unittest.TestCase):

  def setUp(self) -> None:
    helper.clean_up()

  def tearDown(self) -> None:
    helper.clean_up()

  def test_interpolate_without_override(self):
    svc = setup_interp('no_change')
    actual = svc['spec']['ports'][0]['port']
    self.assertEqual(actual, 9000)

  def test_interpolate_with_override(self):
    svc = setup_interp('plus_one')
    actual = svc['spec']['ports'][0]['port']
    self.assertEqual(actual, 9001)
