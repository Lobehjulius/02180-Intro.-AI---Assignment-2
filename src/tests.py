import unittest

from belief_base import BeliefBase
from entailment import entails, is_consistent
from revision import expand, contract, revise


class TestRevision(unittest.TestCase):
    def test_expand(self):
        base = BeliefBase([("p", 3)])
        new_base = expand(base, "q", 2)

        self.assertTrue(entails(new_base, "q"))
        self.assertTrue(entails(new_base, "p"))

    def test_contract(self):
        base = BeliefBase([("p", 3), ("p -> q", 2), ("r", 1)])
        new_base = contract(base, "q")

        self.assertFalse(entails(new_base, "q"))
        self.assertTrue(entails(new_base, "r"))

    def test_revise(self):
        base = BeliefBase([("p", 3), ("p -> ~q", 2)])
        new_base = revise(base, "q", 5)

        self.assertTrue(entails(new_base, "q"))
        self.assertTrue(is_consistent(new_base))

    def test_vacuity_like_case(self):
        base = BeliefBase([("p", 3)])
        new_base = revise(base, "q", 2)

        self.assertTrue(entails(new_base, "p"))
        self.assertTrue(entails(new_base, "q"))

    def test_consistency(self):
        base = BeliefBase([("p", 3), ("p -> ~q", 2)])
        new_base = revise(base, "q", 5)

        self.assertTrue(is_consistent(new_base))


if __name__ == "__main__":
    unittest.main()
