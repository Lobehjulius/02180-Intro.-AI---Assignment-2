from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from belief_revision import BeliefBase


base = BeliefBase([
    ("p", 3),
    ("(p -> q)", 1),
    ("r", 2),
])

print("Original base")
print(base)
print()
print("Revision with ~q")
print(base.revise("~q"))
