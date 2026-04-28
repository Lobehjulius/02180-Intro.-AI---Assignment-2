from itertools import combinations

from cnf import cnf_to_clauses
from node import Not
from parser import parse_formula


def _coerce_formula(formula):
    """
    Accept either an AST formula or a formula string.
    """
    if isinstance(formula, str):
        return parse_formula(formula)
    return formula


def _extract_formulas(base) -> list[object]:
    """
    Accept a BeliefBase, a list of Belief objects, raw formulas, or tuples
    where the formula is stored in position 0.
    """
    if hasattr(base, "formulas") and callable(base.formulas):
        return [_coerce_formula(formula) for formula in base.formulas()]

    formulas = []
    for item in base:
        if hasattr(item, "formula"):
            formulas.append(_coerce_formula(item.formula))
        elif isinstance(item, tuple):
            formulas.append(_coerce_formula(item[0]))
        else:
            formulas.append(_coerce_formula(item))

    return formulas


def complement(literal: str) -> str:
    if literal.startswith("~"):
        return literal[1:]
    return f"~{literal}"


def is_tautology(clause: frozenset[str]) -> bool:
    return any(complement(literal) in clause for literal in clause)


def resolve(clause_a: frozenset[str], clause_b: frozenset[str]) -> set[frozenset[str]]:
    """
    Resolve two clauses on every complementary literal pair they share.
    """
    resolvents = set()

    for literal in clause_a:
        opposite = complement(literal)
        if opposite not in clause_b:
            continue

        resolvent = frozenset((clause_a - {literal}) | (clause_b - {opposite}))
        if not is_tautology(resolvent):
            resolvents.add(resolvent)

    return resolvents


def clauses_from_base(base) -> set[frozenset[str]]:
    clauses = set()
    for formula in _extract_formulas(base):
        clauses |= cnf_to_clauses(formula)
    return clauses


def resolution_refutation(clauses: set[frozenset[str]]) -> bool:
    """
    Return True iff the clause set is unsatisfiable.
    """
    known = set(clauses)

    while True:
        new_clauses = set()

        for clause_a, clause_b in combinations(known, 2):
            for resolvent in resolve(clause_a, clause_b):
                if not resolvent:
                    return True
                if resolvent not in known:
                    new_clauses.add(resolvent)

        if not new_clauses:
            return False

        known |= new_clauses


def entails(base, formula) -> bool:
    """
    Check whether base |= formula using resolution refutation:
        base |= phi iff base and not phi is unsatisfiable
    """
    query = _coerce_formula(formula)
    clauses = clauses_from_base(base)
    clauses |= cnf_to_clauses(Not(query))
    return resolution_refutation(clauses)


def is_consistent(base) -> bool:
    """
    Check whether the formulas in the base are jointly satisfiable.
    """
    return not resolution_refutation(clauses_from_base(base))
