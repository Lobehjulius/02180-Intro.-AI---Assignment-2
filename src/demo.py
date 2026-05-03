from belief_base import BeliefBase
from cnf import cnf_to_clauses
from entailment import entails, is_consistent
from parser import parse_formula
from revision import contract, expand, revise


def print_header(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def print_base(base: BeliefBase) -> None:
    for belief in base.sorted_by_priority():
        print(
            f"formula={belief.formula}, "
            f"priority={belief.priority}, "
            f"source={belief.source}"
        )


def print_queries(base: BeliefBase, formulas: list[str]) -> None:
    for formula in formulas:
        print(f"entails({formula}) = {entails(base, formula)}")


def demo_parser_and_cnf() -> None:
    print_header("Parser And CNF Demo")
    text = "p -> ~q"
    parsed = parse_formula(text)
    clauses = cnf_to_clauses(parsed)

    print(f"input formula: {text}")
    print(f"parsed AST: {parsed!s}")
    print(f"CNF clauses: {clauses}")


def demo_expansion() -> None:
    print_header("Expansion Demo")
    base = BeliefBase([("p", 3), ("r", 1)])
    print("initial belief base:")
    print_base(base)

    expanded = expand(base, "q", 2)
    print()
    print("after expand(base, 'q', 2):")
    print_base(expanded)
    print_queries(expanded, ["p", "q", "r"])
    print(f"is_consistent = {is_consistent(expanded)}")


def demo_contraction() -> None:
    print_header("Contraction Demo")
    base = BeliefBase([("p", 3), ("p -> q", 2), ("r", 1)])
    print("initial belief base:")
    print_base(base)
    print()
    print("before contraction:")
    print_queries(base, ["q", "r"])

    contracted = contract(base, "q")
    print()
    print("after contract(base, 'q'):")
    print_base(contracted)
    print_queries(contracted, ["q", "r"])


def demo_revision() -> None:
    print_header("Revision Demo")
    base = BeliefBase([("p", 3), ("p -> ~q", 2), ("r", 1)])
    print("initial belief base:")
    print_base(base)
    print()
    print("before revision:")
    print_queries(base, ["~q", "q", "r"])
    print(f"is_consistent = {is_consistent(base)}")

    revised = revise(base, "q", 5)
    print()
    print("after revise(base, 'q', 5):")
    print_base(revised)
    print_queries(revised, ["q", "~q", "r"])
    print(f"is_consistent = {is_consistent(revised)}")


def main() -> None:
    print("Belief Revision Assignment Demo")
    print("==============================")
    demo_parser_and_cnf()
    demo_expansion()
    demo_contraction()
    demo_revision()


if __name__ == "__main__":
    main()
