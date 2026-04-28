from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .cnf import ensure_formula
from .formula import Formula, formula_to_string, negate
from .resolution import entails, is_consistent


@dataclass(frozen=True)
class Belief:
    formula: Formula
    text: str
    priority: int
    order: int


class BeliefBase:
    """Finite propositional belief base with priority-guided partial meet contraction.

    The base itself is not deductively closed. Logical consequences are computed on demand
    with resolution. Contraction is computed from remainders and a simple selection function
    induced by the priority order on stored formulas. Revision uses the Levi identity.
    """

    def __init__(self, beliefs: Iterable[tuple[str, int]] | None = None):
        self._beliefs: List[Belief] = []
        self._next_order = 0
        if beliefs is not None:
            for formula_text, priority in beliefs:
                self.add(formula_text, priority)

    @classmethod
    def from_beliefs(cls, beliefs: Sequence[Belief]) -> "BeliefBase":
        base = cls()
        base._beliefs = sorted(list(beliefs), key=lambda belief: belief.order)
        base._next_order = 0 if not base._beliefs else max(belief.order for belief in base._beliefs) + 1
        return base

    def copy(self) -> "BeliefBase":
        return BeliefBase.from_beliefs(self._beliefs)

    @property
    def beliefs(self) -> List[Belief]:
        return list(self._beliefs)

    @property
    def formulas(self) -> List[str]:
        return [belief.text for belief in self._beliefs]

    def max_priority(self) -> int:
        return max((belief.priority for belief in self._beliefs), default=0)

    def add(self, formula_text: str, priority: int = 1) -> None:
        formula = ensure_formula(formula_text)
        canonical = formula_to_string(formula)
        for index, belief in enumerate(self._beliefs):
            if belief.text == canonical:
                if priority > belief.priority:
                    self._beliefs[index] = Belief(belief.formula, belief.text, priority, belief.order)
                return
        self._beliefs.append(Belief(formula, canonical, priority, self._next_order))
        self._next_order += 1

    def entails(self, query: Formula | str) -> bool:
        return entails([belief.formula for belief in self._beliefs], query)

    def is_consistent(self) -> bool:
        return is_consistent([belief.formula for belief in self._beliefs])

    def expand(self, formula_text: str, priority: int | None = None) -> "BeliefBase":
        expanded = self.copy()
        expanded.add(formula_text, expanded.max_priority() + 1 if priority is None else priority)
        return expanded

    def _remainders(self, target: Formula | str) -> List[List[Belief]]:
        target_formula = ensure_formula(target)
        beliefs = self._beliefs
        safe_subsets = []
        for mask in range(1 << len(beliefs)):
            subset = [beliefs[index] for index in range(len(beliefs)) if mask & (1 << index)]
            if not entails([belief.formula for belief in subset], target_formula):
                safe_subsets.append(frozenset(subset))
        maximal = [subset for subset in safe_subsets if not any(subset < other for other in safe_subsets)]
        return [sorted(list(subset), key=lambda belief: belief.order) for subset in maximal]

    def _priority_profile(self, remainder: Sequence[Belief]) -> tuple[int, ...]:
        levels = sorted({belief.priority for belief in self._beliefs}, reverse=True)
        return tuple(sum(1 for belief in remainder if belief.priority == level) for level in levels)

    def _selected_remainders(self, target: Formula | str) -> List[List[Belief]]:
        remainders = self._remainders(target)
        if not remainders:
            return []
        best = max(self._priority_profile(remainder) for remainder in remainders)
        return [remainder for remainder in remainders if self._priority_profile(remainder) == best]

    def contract(self, target: Formula | str) -> "BeliefBase":
        target_formula = ensure_formula(target)
        if not self.entails(target_formula):
            return self.copy()

        selected = self._selected_remainders(target_formula)
        if not selected:
            return self.copy()

        kept = set(selected[0])
        for remainder in selected[1:]:
            kept &= set(remainder)
        return BeliefBase.from_beliefs(sorted(kept, key=lambda belief: belief.order))

    def revise(self, formula_text: str, priority: int | None = None) -> "BeliefBase":
        formula = ensure_formula(formula_text)
        return self.contract(negate(formula)).expand(formula_to_string(formula), priority=priority)

    def equivalent_to(self, other: "BeliefBase") -> bool:
        return all(other.entails(formula) for formula in self.formulas) and all(
            self.entails(formula) for formula in other.formulas
        )

    def as_table(self) -> List[dict[str, int | str]]:
        return [
            {"priority": belief.priority, "formula": belief.text, "order": belief.order}
            for belief in sorted(self._beliefs, key=lambda belief: (-belief.priority, belief.order))
        ]

    def __str__(self) -> str:
        lines = ["Belief base:"]
        for belief in sorted(self._beliefs, key=lambda item: (-item.priority, item.order)):
            lines.append(f"  [priority {belief.priority}] {belief.text}")
        return "\n".join(lines)
