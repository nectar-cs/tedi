import re
import sys
from typing import Optional

from teds import helm, kerbi


def arg_value(name) -> Optional[str]:
  if name in sys.argv:
    index = sys.argv.index(name)
    return sys.argv[index + 1]
  else:
    return None


def extras() -> str:
  expr = arg_value('--args')
  if expr:
    match = re.match("^\[(.*)\]$", expr)
    return match[1] if match is not None else ''
  else:
    return ''


def main():
  if 'kerbi' in sys.argv:
    ted = kerbi
  elif 'helm' in sys.argv:
    ted = helm
  else:
    raise RuntimeError(f"Unrecognized Ted {sys.argv}")

  if 'init' in sys.argv:
    ted.init()
  if 'interpolate' in sys.argv:
    print(ted.interpolate(extras()), flush=True)


if __name__ == '__main__':
  main()
