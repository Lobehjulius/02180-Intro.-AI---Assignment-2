# Belief Revision Assignment

This repository contains a Python implementation for the DTU 02180 Introduction to Artificial Intelligence belief revision assignment.

The project models a finite propositional belief base with priorities and implements:

- propositional formula parsing
- CNF conversion
- logical entailment by resolution refutation
- belief base expansion
- priority-guided contraction
- revision via Levi identity
- unit tests, including AGM-style test cases

## Project Structure

```text
src/
  belief_base.py      Belief and BeliefBase data structures
  cnf.py              CNF conversion and clause extraction
  demo.py             General demo of parser, CNF, expansion, contraction, revision
  entailment.py       Resolution-based entailment and consistency checking
  main.py             Entry point for demo modes
  Mastermind_demo.py  Mastermind-style themed demo
  node.py             AST node definitions for propositional formulas
  parser.py           Formula tokenizer and parser
  revision.py         Expansion, contraction, and revision
  tests.py            Unit tests and AGM-style tests
```

## Running The Project

### General demo

From the project root:

```powershell
python src/main.py demo
```

This shows:

- parsing and CNF conversion
- expansion
- contraction
- revision
- entailment and consistency checks

### Mastermind-style demo

```powershell
python src/main.py mastermind
```

This runs a themed example showing how revision can update a belief base when new clue information conflicts with previous beliefs.

## Running Tests

Run the full test suite from the project root:

```powershell
python src/tests.py
```

The test suite includes:

- basic expansion, contraction, and revision tests
- consistency checks
- AGM-style tests for:
  - success
  - vacuity
  - inclusion
  - consistency
  - extensionality

To run tests in verbose mode, change into the `src` directory and run:

```powershell
cd src
python -m unittest -v tests
```