# Belief Revision Assignment — Getting Started Guide

This note is intended as a clean handoff document for a coding agent.
It summarizes the assignment, the relevant lecture material, and a recommended implementation plan.

---

## 1. What the assignment requires

The default assignment path is:

1. **Design and implement a belief base**
2. **Design and implement a logical entailment checker**
   - Must be implemented by you
   - Do not use an existing package for the reasoning engine
3. **Implement contraction of the belief base**
   - Based on a **priority order on formulas in the belief base**
4. **Implement expansion of the belief base**
5. Output the resulting **new belief base**

The assignment also says the implementation should be based on course methods such as:
- propositional logic
- resolution
- CNF form
- AGM revision
- partial meet contraction

You are also asked to test the algorithm using AGM-style postulates, especially:
- Success
- Inclusion
- Vacuity
- Consistency
- Extensionality

---

## 2. Relevant lecture takeaways

### Lecture 8: Logical Agents
Useful for:
- propositional syntax
- knowledge bases
- entailment
- model checking
- basic logical notions

Important idea:
A knowledge base is a **set of sentences**, and inference should guarantee that what is answered follows from what has been told to the KB.

Useful formal notion:
- `psi |= phi` iff every model of `psi` is also a model of `phi`

### Lecture 9: Belief Revision
Useful for:
- belief sets vs belief bases
- inconsistency
- logical consequence
- contraction, expansion, revision
- Levi identity

Important practical distinction:
- **Belief set** = deductively closed set of consequences (abstract, usually infinite / not practical to store)
- **Belief base** = finite set of explicitly stored formulas

For implementation, you should store a **belief base**, not a full belief set.
Consequences should be computed via the entailment engine when needed.

---

## 3. Recommended implementation strategy

### Recommendation: use the belief-base route
Do **not** implement plausibility orders unless there is a strong reason.
The belief-base version is simpler and maps directly to the assignment stages.

### Recommendation: use Python
Reason:
- easy parsing
- convenient data structures
- fast to prototype and test
- exhaustive search over subsets is feasible for small/medium examples

---

## 4. Core design choice

Use a finite belief base with priorities.

Each belief should store at least:
- the formula
- its priority
- optionally metadata like source / insertion order

Possible structure:

```python
Belief(
    formula=..., 
    priority=..., 
    source="initial" or "new"
)
```

Example:

```python
[
    ("p", 3),
    ("p -> q", 2),
    ("q", 1)
]
```

Interpretation:
- higher priority = harder to remove during contraction

---

## 5. Suggested project structure

```text
parser.py
formula.py
cnf.py
entailment.py
belief_base.py
revision.py
tests.py
main.py
```

### `formula.py`
Implement an AST for propositional formulas, e.g.:
- `Atom(name)`
- `Not(f)`
- `And(f, g)`
- `Or(f, g)`
- `Imp(f, g)`
- `Iff(f, g)`

### `parser.py`
Parse strings such as:
- `p`
- `~p`
- `(p -> q)`
- `((p & q) -> r)`

into AST objects.

### `cnf.py`
Implement CNF conversion.
A standard pipeline is:
1. eliminate biconditionals
2. eliminate implications
3. push negations inward
4. distribute disjunction over conjunction
5. extract clauses

### `entailment.py`
Implement logical entailment.
Recommended method: **resolution refutation**.

Use the equivalence:

`B |= phi` iff `B ∧ ¬phi` is unsatisfiable.

So:
1. convert every formula in `B` to CNF
2. add `¬phi`
3. run resolution
4. if the empty clause is derived, entailment holds

This matches the assignment well because it explicitly mentions CNF and resolution.

### `belief_base.py`
Implement the actual stored belief base.
Typical operations:
- add belief
- remove belief
- list formulas
- sort / compare by priority
- query entailment from the current base

### `revision.py`
Implement:
- expansion
- contraction
- revision

---

## 6. Entailment: recommended implementation details

### Best choice: resolution-based entailment
This is the most assignment-aligned method.

Function goal:

```python
def entails(base, phi) -> bool:
    ...
```

Resolution input representation:
- a clause = a set / frozenset of literals
- a literal = something like `(symbol, is_negated)` or string form like `"p"` / `"~p"`

Example CNF:
- `(p ∨ ~q) ∧ (r ∨ q)`
becomes something like:

```python
{
    frozenset({"p", "~q"}),
    frozenset({"r", "q"})
}
```

### Resolution procedure
Given a set of clauses:
- repeatedly resolve pairs of clauses
- add new resolvents
- stop if the empty clause is produced
- stop if no new clauses can be produced

If the empty clause is derived, the set is unsatisfiable.

---

## 7. Expansion

Expansion is the easy part.

Formal idea:
- add the new formula to the belief base

Possible implementation:

```python
def expand(base, phi, priority):
    return base + [(phi, priority)]
```

Note:
Expansion does **not** by itself guarantee consistency.
It simply adds the new information.

---

## 8. Contraction

This is the nontrivial part.

The assignment asks for contraction based on a **priority order on formulas in the belief base**.
It also mentions **partial meet contraction**.

### Recommended practical version
Implement a **priority-guided partial-meet style contraction**.

Goal:
To contract `B` by `phi`, return a new base that no longer entails `phi`, while removing as little and as low-priority information as possible.

### Conceptual algorithm
1. Generate subsets `S ⊆ B`
2. Keep only those subsets such that:
   - `S` does **not** entail `phi`
3. Among those, keep only **maximal** subsets
   - i.e. remainder-set style candidates
4. Score candidates by priority
   - e.g. sum of retained priorities
5. Choose the best candidate
6. Return that candidate as the contracted base

### Why this is a good choice
It captures the main idea of contraction:
- give up belief in `phi`
- preserve as much of the old base as possible
- preferably keep higher-priority beliefs

### Example intuition
Suppose:

```text
B = { p(3), q(1), p -> ~q(2) }
```

If contracting by `q`, the algorithm should prefer removing the lower-priority belief `q` rather than removing higher-priority formulas when possible.

### Practical note
Enumerating all subsets is exponential.
That is acceptable for a course assignment if the examples are small.
You can document this as a deliberate simplicity/clarity tradeoff.

---

## 9. Revision

The cleanest implementation is to define revision using the **Levi identity**:

`B * phi = (B div ~phi) + phi`

That means:
1. contract the base by `¬phi`
2. expand the result with `phi`

Possible implementation:

```python
def revise(base, phi, priority):
    contracted = contract(base, Not(phi))
    return expand(contracted, phi, priority)
```

This is elegant and directly grounded in the belief revision theory from lecture.

---

## 10. What not to do at first

Do **not** start with:
- Mastermind
- plausibility orders
- GUI / front end
- natural language input
- optimization

First get a correct symbolic implementation working.
The assignment only requires propositional logic in symbolic form.

---

## 11. Minimal milestone plan

### Phase 1
Implement:
- formula AST
- parser
- CNF conversion
- resolution-based entailment

At this stage you should be able to answer queries of the form:
- does the current base entail `phi`?

### Phase 2
Implement:
- expansion
- contraction using priority-guided remainder selection

### Phase 3
Implement:
- revision via Levi identity
- automated tests for core cases

### Phase 4
Add:
- cleaner CLI / demo examples
- report-ready examples
- AGM-postulate tests

---

## 12. AGM-style testing ideas

The assignment specifically asks for tests related to:
- Success
- Inclusion
- Vacuity
- Consistency
- Extensionality

Even if exact formalizations depend on course notation, the implementation should support tests of the following kind.

### Success
After revising by `phi`, the new base should entail `phi`.

```python
assert entails(revise(B, phi, prio), phi)
```

### Inclusion
The revised base should not contain arbitrary unrelated information; it should be based on old beliefs plus what is needed to incorporate `phi`.

### Vacuity
If the old base is already consistent with `phi`, revision by `phi` should behave close to simple expansion.

### Consistency
If `phi` itself is consistent, revising by `phi` should yield a consistent result.

### Extensionality
If `phi` and `psi` are logically equivalent, revising by `phi` and revising by `psi` should give equivalent outcomes.

You may need the lecture 11 notes or course notes for the exact formal postulates expected by the instructor.

---

## 13. Report structure recommendation

The report can follow the assignment stages directly.

### 1. Introduction
Explain:
- what belief revision is
- why inconsistency matters
- why belief bases are used instead of full belief sets

### 2. Formalism / Representation
Describe:
- propositional language
- syntax of formulas
- belief base representation
- priority ordering

### 3. Entailment
Describe:
- CNF transformation
- clause representation
- resolution refutation
- why this proves entailment

### 4. Contraction
Describe:
- goal of contraction
- remainder-style subset selection
- how priority is used to choose what to keep

### 5. Expansion and Revision
Describe:
- expansion as addition
- revision via Levi identity

### 6. Testing
Describe:
- example test cases
- AGM postulate checks

### 7. What we learned
Reflect on:
- belief revision vs ordinary database update
- why inconsistency is problematic
- tradeoff between formal elegance and implementability

### 8. Conclusion / Further work
Mention possible extensions:
- plausibility orders
- more efficient contraction
- Mastermind
- richer input language

---

## 14. Immediate coding priorities

Start by implementing only these functions:

```python
def parse(formula_str) -> Formula:
    ...


def entails(base, phi) -> bool:
    ...


def expand(base, phi, priority):
    ...
```

Then add:

```python
def contract(base, phi):
    ...


def revise(base, phi, priority):
    ...
```

That is the safest path to a working prototype.

---

## 15. Final implementation recommendation

Use this overall approach:

- finite propositional **belief base**
- formulas stored with **priorities**
- **resolution** for entailment
- **priority-guided contraction**
- **revision via Levi identity**

This is theoretically grounded, straightforward to explain in the report, and realistic to implement within a course assignment.
