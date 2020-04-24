import sys

from teds import helm, kerbi, utils


def main():
  if len(sys.argv) < 2:
    raise RuntimeError(f"Missing args")

  ted_type = sys.argv[1]
  op_name = sys.argv[2]

  if ted_type == 'kerbi':
    ted = helm
  elif ted_type == 'helm':
    ted = kerbi
  else:
    raise RuntimeError(f"Unrecognized Ted {ted_type}")

  if op_name == 'init':
    utils.init()
  elif op_name == 'interpolate':
    ted.interpolate()


if __name__ == '__main__':
  main()
