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

<!-- 
## Approach

The implementation follows a belief-base approach rather than a deductively closed belief-set approach.

- Beliefs are stored explicitly in a finite `BeliefBase`
- Each belief has a propositional formula and a priority
- Logical consequences are computed on demand using entailment
- Contraction is implemented by generating subsets of the belief base, keeping those that do not entail the target formula, selecting maximal candidates, and then choosing the best one using retained priorities
- Revision is implemented using Levi identity:

```text
revise(B, phi) = expand(contract(B, not phi), phi)
```
-->
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

<!-- 
## Main Data Model

The belief base is represented as a finite collection of prioritized formulas:

```text
B = {(phi_1, p_1), (phi_2, p_2), ..., (phi_n, p_n)}
```

where:

- `phi_i` is a propositional formula
- `p_i` is a priority

Higher priority means the belief is preferred for retention during contraction.

The implementation is not deductively closed. A formula is accepted only if it is entailed by the stored base.
-->
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
<!-- 
## Example

Consider the belief base:

```text
{p, p -> ~q, r}
```

If the system is revised by `q`, it first contracts the base by `~q`, then adds `q`.

The result is a new base that:

- entails `q`
- no longer entails `~q`
- preserves as much of the original belief base as possible
- prefers to keep higher-priority beliefs

## Limitations

This project is designed for clarity and alignment with the assignment, not for large-scale performance.

- contraction enumerates subsets of the belief base
- this is exponential in the number of beliefs
- priorities are assigned manually
- formulas that are logically equivalent may still be stored in different syntactic forms

These tradeoffs are acceptable for a course assignment and make the implementation easier to explain and test.

## Authors

DTU 02180 Introduction to Artificial Intelligence Assignment 2 project group.
-->