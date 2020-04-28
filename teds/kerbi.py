from teds import utils as ut


def init():
  if ut.init():
    command = f"~/.rbenv/bin/rbenv exec bundle"
    ut.exec_cmd(command, cwd=ut.working_dir())


def interpolate():
  paths = [ut.values_path(), ut.overrides_path()]
  real_paths = [p for p in paths if p]
  f_paths = " -f ".join(real_paths)
  command = f"~/.rbenv/bin/rbenv exec ruby app.rb -f {f_paths}"
  return ut.exec_cmd(command, cwd=ut.working_dir())
