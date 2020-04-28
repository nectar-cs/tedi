from teds import utils as ut
import subprocess


def init():
  ut.init()


def bundle_gems():
  command = f"~/.rbenv/bin/rbenv exec bundle"
  ut.exec_cmd(command, cwd=ut.working_dir(), stderr=subprocess.DEVNULL)


def interpolate():
  bundle_gems()
  paths = [ut.values_path(), ut.overrides_path()]
  real_paths = [p for p in paths if p]
  f_paths = " -f ".join(real_paths)
  command = f"~/.rbenv/bin/rbenv exec ruby app.rb -f {f_paths}"
  return ut.exec_cmd(command, cwd=ut.working_dir())
