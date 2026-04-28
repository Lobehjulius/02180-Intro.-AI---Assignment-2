# Belief Revision Assignment - Source Code

This folder contains a small Python implementation of the assignment in the course sequence:

1. a finite belief base,
2. self-implemented entailment by CNF conversion and propositional resolution,
3. contraction by priority-guided partial meet,
4. non-closing expansion and revision via the Levi identity,
5. the optional Mastermind part as a simple possible-world code-breaker.

The code only uses the Python standard library.

## Project structure

- `belief_revision/` - package with parser, CNF, resolution, belief revision, and Mastermind
- `tests/` - unit tests, including AGM-style checks and a small Mastermind test
- `examples/demo.py` - minimal belief revision example
- `examples/mastermind_demo.py` - optional Mastermind example
- `pyproject.toml` - minimal package metadata

## Installation

From this `source/` folder:

```bash
python -m pip install -e .
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Example: belief revision

```bash
python -m belief_revision.cli revise --revise "~q"
```

With explicit beliefs:

```bash
python -m belief_revision.cli revise \
  --belief "p::3" \
  --belief "(p -> q)::1" \
  --belief "r::2" \
  --revise "~q"
```

## Example: optional Mastermind

```bash
python -m belief_revision.cli mastermind --secret 1234
```

This runs the optional code-breaker for the traditional 4-peg, 6-color setting.
The Mastermind part is intentionally simple: the current belief state is the set of
candidate codes still compatible with the feedback received so far.

## Main implementation choices

- The belief state is a **belief base**, not a deductively closed belief set.
- Entailment is checked on demand by **resolution refutation**.
- Contraction computes **remainders** and keeps the remainders with the best
  retained priority profile.
- The final contracted base is the **intersection of the selected remainders**.
- Revision is **internal revision on a belief base**:
  `B * phi = (B - ~phi) + phi`.
- The optional Mastermind solver uses the same belief-change idea in a finite
  possible-world space: feedback removes impossible worlds.
