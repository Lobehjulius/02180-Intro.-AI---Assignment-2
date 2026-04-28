from __future__ import annotations

from typing import Iterable, List, Set

from .cnf import Clause, formulas_to_clauses, ensure_formula
from .formula import Formula, Not


def is_tautology(clause: Clause) -> bool:
    return any((name, not value) in clause for name, value in clause)


def resolve(left: Clause, right: Clause) -> Set[Clause]:
    resolvents: Set[Clause] = set()
    for literal in left:
        complement = (literal[0], not literal[1])
        if complement in right:
            resolvent = frozenset((left - {literal}) | (right - {complement}))
            if not is_tautology(resolvent):
                resolvents.add(resolvent)
    return resolvents


def resolution_unsat(clauses: Iterable[Clause]) -> bool:
    clause_set: Set[Clause] = {frozenset(clause) for clause in clauses if not is_tautology(clause)}
    if frozenset() in clause_set:
        return True

    processed_pairs: Set[tuple[Clause, Clause]] = set()
    while True:
        new: Set[Clause] = set()
        clause_list = list(clause_set)
        for index, left in enumerate(clause_list):
            for right in clause_list[index + 1 :]:
                pair = (left, right) if left <= right else (right, left)
                if pair in processed_pairs:
                    continue
                processed_pairs.add(pair)
                resolvents = resolve(left, right)
                if frozenset() in resolvents:
                    return True
                new.update(resolvents - clause_set)
        if not new:
            return False
        clause_set.update(new)


def entails(premises: List[Formula | str], query: Formula | str) -> bool:
    query_formula = ensure_formula(query)
    premises_clauses = formulas_to_clauses(premises)
    negated_query_clauses = formulas_to_clauses([Not(query_formula)])
    return resolution_unsat(premises_clauses + negated_query_clauses)


def is_consistent(formulas: List[Formula | str]) -> bool:
    return not resolution_unsat(formulas_to_clauses(formulas))
