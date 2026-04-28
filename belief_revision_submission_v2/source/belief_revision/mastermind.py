from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from itertools import product
from typing import Iterable, List, Sequence, Tuple

Code = Tuple[int, ...]
Feedback = Tuple[int, int]  # (black, white)


def all_codes(pegs: int = 4, colors: int = 6) -> List[Code]:
    return list(product(range(1, colors + 1), repeat=pegs))


def score(secret: Sequence[int], guess: Sequence[int]) -> Feedback:
    black = sum(secret_pin == guess_pin for secret_pin, guess_pin in zip(secret, guess))
    secret_counts = Counter(secret)
    guess_counts = Counter(guess)
    white = sum(min(secret_counts[color], guess_counts[color]) for color in secret_counts) - black
    return black, white


@dataclass
class MastermindAgent:
    """Simple code-breaker based on possible worlds.

    The current belief state is the finite set of candidate codes still compatible with all
    observed feedback. This mirrors the possible-world view of belief change while keeping the
    optional assignment short and computationally transparent.
    """

    pegs: int = 4
    colors: int = 6
    first_guess: Code | None = None
    candidates: List[Code] = field(default_factory=list)
    history: List[tuple[Code, Feedback]] = field(default_factory=list)
    current_guess: Code | None = None

    def reset(self) -> None:
        self.candidates = all_codes(self.pegs, self.colors)
        self.history = []
        self.current_guess = self.first_guess or self.candidates[0]

    def start(self) -> Code:
        if not self.candidates:
            self.reset()
        if self.current_guess is None:
            self.current_guess = self.first_guess or self.candidates[0]
        return self.current_guess

    def revise(self, feedback: Feedback) -> Code | None:
        if self.current_guess is None:
            raise ValueError("Call start() before revise().")
        guess = self.current_guess
        self.history.append((guess, feedback))
        self.candidates = [code for code in self.candidates if score(code, guess) == feedback]
        self.current_guess = self.candidates[0] if self.candidates else None
        return self.current_guess

    def solve(self, secret: Iterable[int]) -> List[dict[str, object]]:
        secret_code = tuple(secret)
        self.reset()
        transcript: List[dict[str, object]] = []
        guess = self.start()
        while guess is not None:
            feedback = score(secret_code, guess)
            step = {"guess": guess, "feedback": feedback}
            if feedback[0] == self.pegs:
                step["remaining_candidates"] = len(self.candidates)
                transcript.append(step)
                return transcript
            guess = self.revise(feedback)
            step["remaining_candidates"] = len(self.candidates)
            transcript.append(step)
        return transcript

    def beliefs(self) -> List[Code]:
        return list(self.candidates)


def format_code(code: Sequence[int]) -> str:
    return "".join(str(pin) for pin in code)
