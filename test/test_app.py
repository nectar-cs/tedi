import sys
import unittest

import app


class TestApp(unittest.TestCase):

  def test_arg_value(self):
    sys.argv = ['-x', 'y', '-y', 'z']
    self.assertEqual(app.arg_value('-x'), 'y')
    self.assertEqual(app.arg_value('-y'), 'z')

  def test_extras_valid_args(self):
    sys.argv = ['--args', '[-x y --y z]']
    self.assertEqual(app.extras(), "-x y --y z")

  def test_extras_invalid_args(self):
    sys.argv = ['--args', '[-x y']
    self.assertEqual(app.extras(), "")
