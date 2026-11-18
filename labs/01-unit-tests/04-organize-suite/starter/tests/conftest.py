"""Shared fixtures for the tests of cart.py. Task 2 moves them here."""

# --- Mutant hunt: leave this part as it is ---------------------------------
# When CART_MUTANT names a folder in tests/mutants/, that folder goes first on
# the import path, so `import cart` loads the mutant. It must run before the
# imports below.
import os
import sys
from pathlib import Path

_mutant = os.environ.get("CART_MUTANT")
if _mutant:
    sys.path.insert(0, str(Path(__file__).parent / "mutants" / _mutant))
# ---------------------------------------------------------------------------
