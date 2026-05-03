from belief_base import BeliefBase
from entailment import entails, is_consistent
from revision import revise


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


def main() -> None:
    print("Mastermind-Style Belief Revision Demo")
    print("=====================================")
    print("This is a themed revision scenario, not a full Mastermind engine.")

    base = BeliefBase(
        [
            ("red_pos1", 3),
            ("red_pos1 -> ~blue_pos1", 3),
            ("green_pos2", 2),
        ]
    )

    print_header("Initial Guess Beliefs")
    print_base(base)
    print(f"entails(red_pos1) = {entails(base, 'red_pos1')}")
    print(f"entails(blue_pos1) = {entails(base, 'blue_pos1')}")
    print(f"is_consistent = {is_consistent(base)}")

    print_header("New Clue")
    print("We now revise the belief base with the clue: blue_pos1")

    revised = revise(base, "blue_pos1", 5)

    print_header("Beliefs After Revision")
    print_base(revised)
    print(f"entails(red_pos1) = {entails(revised, 'red_pos1')}")
    print(f"entails(blue_pos1) = {entails(revised, 'blue_pos1')}")
    print(f"entails(green_pos2) = {entails(revised, 'green_pos2')}")
    print(f"is_consistent = {is_consistent(revised)}")


if __name__ == "__main__":
    main()
