import unittest

from belief_revision import BeliefBase


class BeliefRevisionTests(unittest.TestCase):
    def test_priority_guided_partial_meet_contraction(self) -> None:
        base = BeliefBase([
            ("p", 2),
            ("q", 1),
            ("((p & q) -> r)", 1),
        ])
        contracted = base.contract("r")
        self.assertEqual(contracted.formulas, ["p"])

    def test_success_postulate(self) -> None:
        base = BeliefBase([
            ("p", 3),
            ("(p -> q)", 1),
            ("r", 2),
        ])
        revised = base.revise("~q")
        self.assertTrue(revised.entails("~q"))

    def test_inclusion_postulate(self) -> None:
        base = BeliefBase([
            ("p", 3),
            ("(p -> q)", 1),
            ("r", 2),
        ])
        revised = base.revise("~q")
        allowed = {"p", "p -> q", "r", "~q", "(p -> q)"}
        self.assertTrue(set(revised.formulas).issubset(allowed))

    def test_vacuity_postulate(self) -> None:
        base = BeliefBase([
            ("p", 3),
            ("(p -> q)", 1),
            ("r", 2),
        ])
        self.assertEqual(base.revise("s").formulas, base.expand("s").formulas)

    def test_consistency_postulate(self) -> None:
        base = BeliefBase([
            ("p", 3),
            ("(p -> q)", 1),
            ("r", 2),
        ])
        self.assertTrue(base.revise("~q").is_consistent())

    def test_extensionality_postulate(self) -> None:
        base = BeliefBase([
            ("p", 3),
            ("(p -> q)", 1),
            ("r", 2),
        ])
        self.assertTrue(base.revise("q").equivalent_to(base.revise("~~q")))


if __name__ == "__main__":
    unittest.main()
