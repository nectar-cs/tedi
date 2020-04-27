import sys

from teds import helm, kerbi, utils


def main():
  if len(sys.argv) < 2:
    raise RuntimeError(f"Missing args")

  ted_type = sys.argv[1]

  if ted_type == 'kerbi':
    ted = kerbi
  elif ted_type == 'helm':
    ted = helm
  else:
    raise RuntimeError(f"Unrecognized Ted {ted_type}")

  if 'init' in sys.argv:
    print(ted.init())
  if 'interpolate' in sys.argv:
    print(ted.interpolate())


if __name__ == '__main__':
  main()
