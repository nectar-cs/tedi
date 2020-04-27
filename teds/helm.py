from teds import utils as ut

def init():
  ut.init()


def interpolate():
  paths = [ut.values_path(), ut.overrides_path()]
  real_paths = [p for p in paths if p]
  f_paths = " -f ".join(real_paths)
  command = f"helm template {ut.working_dir()} -f {f_paths}"
  return ut.exec_cmd(command).replace('RELEASE-NAME-', '')
