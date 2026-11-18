"""Lets the mutant hunt swap roster.py for a mutant. You do not need to change it.

When the ROSTER_MUTANT environment variable names a folder in tests/mutants/,
that folder goes first on the import path, so `import roster` loads the mutant.
"""

import os
import sys
from pathlib import Path

_mutant = os.environ.get("ROSTER_MUTANT")
if _mutant:
    sys.path.insert(0, str(Path(__file__).parent / "mutants" / _mutant))
