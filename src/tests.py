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


class TestAGMPostulates(unittest.TestCase):
    def test_success(self):
        base = BeliefBase([("p", 3), ("p -> ~q", 2)])
        new_base = revise(base, "q", 5)
        
        self.assertTrue(entails(new_base, "q"))

    def test_vacuity(self):
        base = BeliefBase([("p", 3)])
        revised = revise(base, "q", 2)
        expanded = expand(base, "q", 2)
        
        self.assertEqual(revised.beliefs(), expanded.beliefs())

    # revised base should not invent unrelated beliefs
    def test_inclusion(self):
        base = BeliefBase([("p", 3)])
        revised = revise(base, "q", 2)
        
        self.assertFalse(entails(revised, "r"))

    def test_consistency(self):
        base = BeliefBase([("p", 3), ("p -> ~q", 2)])
        new_base = revise(base, "q", 5)
        self.assertTrue(is_consistent(new_base))
        
    def test_extensionality_1(self):
        base = BeliefBase([("p", 3), ("p -> ~q", 2)])
        new_base1 = revise(base, "q", 5)
        new_base2 = revise(base, "q", 5)
        
        self.assertEqual(new_base1.beliefs(), new_base2.beliefs())

    def test_extensionality_2(self):
        base = BeliefBase([("p", 3)])
        by_q = revise(base, "q", 2)
        by_notnotq = revise(base, "~~q", 2)

        # sinde "q" and "~~q" are equivalent. the test is checking syntactic equality while AGM extensionally is about logical equivalence 
        # self.assertEqual(by_q.beliefs(), by_notnotq.beliefs())
        # new way of checking extensionality by checking logical equivalence of the beliefs in the revised bases
        self.assertTrue(entails(by_q, "q"))
        self.assertTrue(entails(by_notnotq, "q"))
        self.assertTrue(entails(by_q, "p"))
        self.assertTrue(entails(by_notnotq, "p"))
        self.assertEqual(is_consistent(by_q), is_consistent(by_notnotq))
    
if __name__ == "__main__":
    unittest.main()
