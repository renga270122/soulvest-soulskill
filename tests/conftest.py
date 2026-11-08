"""Shared test configuration for importing repository-root modules."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_string = str(ROOT)
if root_string not in sys.path:
    sys.path.insert(0, root_string)
