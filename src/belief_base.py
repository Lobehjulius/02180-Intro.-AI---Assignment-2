from dataclasses import dataclass
from typing import Iterable, Iterator

from parser import parse_formula


def _coerce_formula(formula):
    """
    Accept either an AST formula or a formula string.
    """
    if isinstance(formula, str):
        return parse_formula(formula)
    return formula


@dataclass(frozen=True)
class Belief:
    formula: object
    priority: int = 0
    source: str = "manual"


class BeliefBase:
    """
    Finite belief base with explicit priorities.
    """

    def __init__(self, beliefs: Iterable[Belief | tuple] | None = None):
        self._beliefs: list[Belief] = []
        if beliefs is not None:
            self.extend(beliefs)

    def add(self, formula, priority: int = 0, source: str = "manual") -> Belief:
        belief = Belief(_coerce_formula(formula), priority, source)
        self._beliefs.append(belief)
        return belief

    def extend(self, beliefs: Iterable[Belief | tuple]) -> None:
        for item in beliefs:
            if isinstance(item, Belief):
                self._beliefs.append(item)
                continue

            if len(item) == 2:
                formula, priority = item
                source = "manual"
            elif len(item) == 3:
                formula, priority, source = item
            else:
                raise ValueError(
                    "Belief tuples must have shape (formula, priority) "
                    "or (formula, priority, source)"
                )

            self.add(formula, priority, source)

    def remove(self, formula) -> Belief:
        target = _coerce_formula(formula)

        for index, belief in enumerate(self._beliefs):
            if belief.formula == target:
                return self._beliefs.pop(index)

        raise ValueError(f"Formula not found in belief base: {target}")

    def discard(self, formula) -> bool:
        try:
            self.remove(formula)
            return True
        except ValueError:
            return False

    def copy(self) -> "BeliefBase":
        return BeliefBase(self._beliefs)

    def formulas(self) -> list[object]:
        return [belief.formula for belief in self._beliefs]

    def priorities(self) -> list[int]:
        return [belief.priority for belief in self._beliefs]

    def beliefs(self) -> list[Belief]:
        return list(self._beliefs)

    def sorted_by_priority(self, reverse: bool = True) -> list[Belief]:
        return sorted(self._beliefs, key=lambda belief: belief.priority, reverse=reverse)

    def entails(self, formula) -> bool:
        from entailment import entails

        return entails(self, formula)

    def __iter__(self) -> Iterator[Belief]:
        return iter(self._beliefs)

    def __len__(self) -> int:
        return len(self._beliefs)

    def __getitem__(self, index: int) -> Belief:
        return self._beliefs[index]

    def __repr__(self) -> str:
        return f"BeliefBase({self._beliefs!r})"
