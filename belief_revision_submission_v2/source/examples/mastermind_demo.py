from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from belief_revision import MastermindAgent, format_code


agent = MastermindAgent(pegs=4, colors=6)
transcript = agent.solve((1, 2, 3, 4))

for turn, step in enumerate(transcript, start=1):
    black, white = step["feedback"]
    print(
        f"Turn {turn}: guess {format_code(step['guess'])} -> "
        f"feedback ({black} black, {white} white), "
        f"remaining {step['remaining_candidates']}"
    )
