"""Entry point for `python -m splitbill`. Output is always UTF-8, whatever the console uses."""

import sys

from .cli import main

for stream in (sys.stdout, sys.stderr):
    stream.reconfigure(encoding="utf-8")

raise SystemExit(main())
