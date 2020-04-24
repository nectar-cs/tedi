from teds import utils as ut


def interpolate():
  f_paths = " -f ".join([ut.values_path(), ut.overrides_path()])
  command = f"ruby app.py {ut.working_dir()} -f {f_paths}"
  return ut.exec_cmd(command)
