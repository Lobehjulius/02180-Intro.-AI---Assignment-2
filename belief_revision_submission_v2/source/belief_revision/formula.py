from __future__ import annotations

from dataclasses import dataclass


class Formula:
    """Marker base class for propositional formulas."""


@dataclass(frozen=True)
class Var(Formula):
    name: str


@dataclass(frozen=True)
class Const(Formula):
    value: bool


@dataclass(frozen=True)
class Not(Formula):
    operand: Formula


@dataclass(frozen=True)
class And(Formula):
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Or(Formula):
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Implies(Formula):
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Iff(Formula):
    left: Formula
    right: Formula


_PRECEDENCE = {
    Iff: 1,
    Implies: 2,
    Or: 3,
    And: 4,
    Not: 5,
    Var: 6,
    Const: 6,
}


def precedence(formula: Formula) -> int:
    return _PRECEDENCE[type(formula)]


def formula_to_string(formula: Formula) -> str:
    """Return a canonical ASCII rendering of a formula."""

    def render(node: Formula, parent_prec: int = 0) -> str:
        if isinstance(node, Var):
            return node.name
        if isinstance(node, Const):
            return "TRUE" if node.value else "FALSE"
        if isinstance(node, Not):
            inner = render(node.operand, precedence(node))
            text = f"~{inner}"
        elif isinstance(node, And):
            text = f"{render(node.left, precedence(node))} & {render(node.right, precedence(node))}"
        elif isinstance(node, Or):
            text = f"{render(node.left, precedence(node))} | {render(node.right, precedence(node))}"
        elif isinstance(node, Implies):
            text = f"{render(node.left, precedence(node))} -> {render(node.right, precedence(node) - 1)}"
        elif isinstance(node, Iff):
            text = f"{render(node.left, precedence(node))} <-> {render(node.right, precedence(node))}"
        else:
            raise TypeError(f"Unsupported formula type: {type(node)!r}")

        if precedence(node) < parent_prec:
            return f"({text})"
        return text

    return render(formula)


def negate(formula: Formula) -> Formula:
    return Not(formula)
