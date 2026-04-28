from __future__ import annotations

import argparse
from typing import List, Tuple

from .belief_base import BeliefBase
from .mastermind import MastermindAgent, format_code


DEFAULT_BELIEFS: List[Tuple[str, int]] = [
    ("p", 3),
    ("(p -> q)", 1),
    ("r", 2),
]


def _parse_belief(specification: str) -> Tuple[str, int]:
    if "::" not in specification:
        raise argparse.ArgumentTypeError("Use 'FORMULA::PRIORITY', e.g. '(p -> q)::1'.")
    formula_text, priority_text = specification.rsplit("::", 1)
    try:
        return formula_text.strip(), int(priority_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Priority must be an integer.") from error


def _parse_code(text: str) -> Tuple[int, ...]:
    if not text.isdigit():
        raise argparse.ArgumentTypeError("Codes must be digit strings, e.g. 1234.")
    return tuple(int(digit) for digit in text)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Belief revision assignment demos.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    revise_parser = subparsers.add_parser("revise", help="Revise a propositional belief base.")
    revise_parser.add_argument("--belief", action="append", type=_parse_belief, default=[])
    revise_parser.add_argument("--revise", required=True, help="Formula used for revision.")
    revise_parser.add_argument("--priority", type=int, default=None)

    mastermind_parser = subparsers.add_parser("mastermind", help="Run the optional Mastermind solver.")
    mastermind_parser.add_argument("--secret", type=_parse_code, required=True, help="Secret code, e.g. 1234.")
    mastermind_parser.add_argument("--colors", type=int, default=6)
    mastermind_parser.add_argument("--first-guess", type=_parse_code, default=None)
    return parser


def main() -> None:
    args = _build_parser().parse_args()

    if args.command == "revise":
        beliefs = args.belief if args.belief else DEFAULT_BELIEFS
        base = BeliefBase(beliefs)
        revised = base.revise(args.revise, priority=args.priority)
        print("Original base")
        print(base)
        print()
        print(f"Revision input: {args.revise}")
        print()
        print("Revised base")
        print(revised)
        return

    agent = MastermindAgent(pegs=len(args.secret), colors=args.colors, first_guess=args.first_guess)
    transcript = agent.solve(args.secret)
    print(f"Secret: {format_code(args.secret)}")
    print()
    for turn, step in enumerate(transcript, start=1):
        black, white = step["feedback"]
        print(
            f"Turn {turn}: guess {format_code(step['guess'])} -> "
            f"feedback ({black} black, {white} white), "
            f"remaining {step['remaining_candidates']}"
        )


if __name__ == "__main__":
    main()
