import unittest

from belief_revision import MastermindAgent, score


class MastermindTests(unittest.TestCase):
    def test_feedback(self) -> None:
        self.assertEqual(score((1, 2, 3, 4), (1, 4, 2, 5)), (1, 2))

    def test_solver_finds_secret_on_small_instance(self) -> None:
        agent = MastermindAgent(pegs=3, colors=4)
        transcript = agent.solve((1, 2, 3))
        self.assertEqual(transcript[-1]["guess"], (1, 2, 3))
        self.assertLessEqual(len(transcript), 64)


if __name__ == "__main__":
    unittest.main()
