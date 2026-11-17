"""Lets the mutant hunt swap passwords.py for a variant. You do not need to change it.

When the PASSWORDS_MUTANT environment variable names a folder in tests/mutants/,
that folder goes first on the import path, so `import passwords` loads the variant.
"""

import os
import sys
from pathlib import Path

_mutant = os.environ.get("PASSWORDS_MUTANT")
if _mutant:
    sys.path.insert(0, str(Path(__file__).parent / "mutants" / _mutant))
