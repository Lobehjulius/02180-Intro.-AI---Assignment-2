zqfrom __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

from .formula import And, Const, Formula, Iff, Implies, Not, Or, Var
from .parser import parse_formula

Literal = Tuple[str, bool]
Clause = frozenset[Literal]


def ensure_formula(formula: Formula | str) -> Formula:
    if isinstance(formula, str):
        return parse_formula(formula)
    return formula


def eliminate_implications(formula: Formula) -> Formula:
    if isinstance(formula, (Var, Const)):
        return formula
    if isinstance(formula, Not):
        return Not(eliminate_implications(formula.operand))
    if isinstance(formula, And):
        return And(eliminate_implications(formula.left), eliminate_implications(formula.right))
    if isinstance(formula, Or):
        return Or(eliminate_implications(formula.left), eliminate_implications(formula.right))
    if isinstance(formula, Implies):
        return Or(Not(eliminate_implications(formula.left)), eliminate_implications(formula.right))
    if isinstance(formula, Iff):
        left = eliminate_implications(formula.left)
        right = eliminate_implications(formula.right)
        return And(Or(Not(left), right), Or(Not(right), left))
    raise TypeError(f"Unsupported formula type: {type(formula)!r}")


def _make_and(left: Formula, right: Formula) -> Formula:
    if isinstance(left, Const):
        return right if left.value else Const(False)
    if isinstance(right, Const):
        return left if right.value else Const(False)
    return And(left, right)


def _make_or(left: Formula, right: Formula) -> Formula:
    if isinstance(left, Const):
        return Const(True) if left.value else right
    if isinstance(right, Const):
        return Const(True) if right.value else left
    return Or(left, right)


def to_nnf(formula: Formula) -> Formula:
    formula = eliminate_implications(formula)
    if isinstance(formula, (Var, Const)):
        return formula
    if isinstance(formula, Not):
        operand = formula.operand
        if isinstance(operand, Var):
            return formula
        if isinstance(operand, Const):
            return Const(not operand.value)
        if isinstance(operand, Not):
            return to_nnf(operand.operand)
        if isinstance(operand, And):
            return _make_or(to_nnf(Not(operand.left)), to_nnf(Not(operand.right)))
        if isinstance(operand, Or):
            return _make_and(to_nnf(Not(operand.left)), to_nnf(Not(operand.right)))
        raise TypeError(f"Unexpected operand under negation: {type(operand)!r}")
    if isinstance(formula, And):
        return _make_and(to_nnf(formula.left), to_nnf(formula.right))
    if isinstance(formula, Or):
        return _make_or(to_nnf(formula.left), to_nnf(formula.right))
    raise TypeError(f"Unexpected formula in NNF conversion: {type(formula)!r}")


def _distribute_or(left: Formula, right: Formula) -> Formula:
    if isinstance(left, And):
        return _make_and(_distribute_or(left.left, right), _distribute_or(left.right, right))
    if isinstance(right, And):
        return _make_and(_distribute_or(left, right.left), _distribute_or(left, right.right))
    return _make_or(left, right)


def to_cnf(formula: Formula | str) -> Formula:
    formula = to_nnf(ensure_formula(formula))
    if isinstance(formula, And):
        return _make_and(to_cnf(formula.left), to_cnf(formula.right))
    if isinstance(formula, Or):
        return _distribute_or(to_cnf(formula.left), to_cnf(formula.right))
    return formula


def _extract_clause(formula: Formula) -> set[Literal]:
    if isinstance(formula, Or):
        return _extract_clause(formula.left) | _extract_clause(formula.right)
    if isinstance(formula, Var):
        return {(formula.name, True)}
    if isinstance(formula, Not) and isinstance(formula.operand, Var):
        return {(formula.operand.name, False)}
    if isinstance(formula, Const):
        if formula.value:
            return set()
        return set()
    raise TypeError(f"Formula is not a CNF clause literal/disjunction: {formula!r}")


def cnf_to_clauses(formula: Formula | str) -> List[Clause]:
    formula = to_cnf(formula)
    if isinstance(formula, Const):
        return [] if formula.value else [frozenset()]
    if isinstance(formula, And):
        return cnf_to_clauses(formula.left) + cnf_to_clauses(formula.right)
    return [frozenset(_extract_clause(formula))]


def formulas_to_clauses(formulas: Sequence[Formula | str] | Iterable[Formula | str]) -> List[Clause]:
    clauses: List[Clause] = []
    for formula in formulas:
        clauses.extend(cnf_to_clauses(formula))
    return clauses
