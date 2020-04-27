from teds import utils as ut




def init():
  if ut.init():
    command = f"bundle"
    result = ut.exec_cmd(command, cwd=ut.working_dir())
    print(result)


def interpolate():
  paths = [ut.values_path(), ut.overrides_path()]
  print(paths)
  real_paths = [p for p in paths if p]
  f_paths = " -f ".join(real_paths)
  command = f"ruby app.rb -f {f_paths}"
  print(command)
  print(ut.exec_cmd("ls", cwd=ut.working_dir()))
  return ut.exec_cmd(command, cwd=ut.working_dir())
