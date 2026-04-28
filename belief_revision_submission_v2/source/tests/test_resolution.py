import unittest

from belief_revision import entails, is_consistent


class ResolutionTests(unittest.TestCase):
    def test_modus_ponens(self) -> None:
        self.assertTrue(entails(["p", "p -> q"], "q"))

    def test_non_entailment(self) -> None:
        self.assertFalse(entails(["p | q"], "p"))

    def test_consistency(self) -> None:
        self.assertTrue(is_consistent(["p", "p -> q", "r"]))
        self.assertFalse(is_consistent(["p", "~p"]))


if __name__ == "__main__":
    unittest.main()
