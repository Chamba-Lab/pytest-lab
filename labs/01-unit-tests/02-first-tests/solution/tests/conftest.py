"""Lets the mutant hunt swap grades.py for a mutant. You do not need to change it.

When the GRADES_MUTANT environment variable names a folder in tests/mutants/,
that folder goes first on the import path, so `import grades` loads the mutant.
"""

import os
import sys
from pathlib import Path

_mutant = os.environ.get("GRADES_MUTANT")
if _mutant:
    sys.path.insert(0, str(Path(__file__).parent / "mutants" / _mutant))
