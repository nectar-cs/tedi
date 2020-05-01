import sys

from teds import helm, kerbi


def main():

  print("Here's what I'm seeing")
  print(sys.argv)

  if 'kerbi' in sys.argv:
    ted = kerbi
  elif 'helm' in sys.argv:
    ted = helm
  else:
    raise RuntimeError(f"Unrecognized Ted {sys.argv}")

  if 'init' in sys.argv:
    print(ted.init())
  if 'interpolate' in sys.argv:
    print(ted.interpolate(), flush=True)


if __name__ == '__main__':
  main()
