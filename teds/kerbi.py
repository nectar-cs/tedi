from teds import utils as ut
import subprocess


def init():
  ut.init()


def bundle_gems():
  command = f"~/.rbenv/bin/rbenv exec bundle"
  ut.exec_cmd(command, cwd=ut.working_dir(), stderr=subprocess.DEVNULL)


def interpolate(extras=''):
  bundle_gems()
  overrides_flag = ut.overrides_path() and f"-f {ut.overrides_path()}"
  command = f"~/.rbenv/bin/rbenv exec ruby main.rb {overrides_flag} {extras}"
  return ut.exec_cmd(command, cwd=ut.working_dir())
