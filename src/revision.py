from belief_base import BeliefBase
from entailment import entails
from itertools import combinations
from node import Not
from parser import parse_formula


def expand(base, formula, priority, source="new"):
    new_base = base.copy()
    new_base.add(formula, priority, source)
    return new_base

def all_subsets(base):
    beliefs = list(base)
    for r in range(len(beliefs), -1, -1):
        for combo in combinations(beliefs, r):
            yield BeliefBase(combo)

# Logical filtering functions
def filter_non_entailing_subsets(base, formula):
    return [
        subset
        for subset in all_subsets(base)
        if not entails(subset, formula)
    ]

def is_maximal(candidate, candidates):
    candidate_set = set(candidate.beliefs())
    return not any(
        candidate_set < set(other.beliefs())
        for other in candidates
    )

# Preserves the as much of the original base as possible, 
# while ensuring the formula is not entailed
def keep_only_max_candidates(base, formula):
    candidates = filter_non_entailing_subsets(base, formula)
    return [c for c in candidates if is_maximal(c, candidates)]

# Preserve the most important beliefs
def score_candidate(candidate):
    return (sum(belief.priority for belief in candidate), len(candidate))

def best_candidates(candidates):
    best = max(candidates, key=score_candidate)
    return best

# Contraction function
def contract(base, formula):
    if not entails(base, formula):
        return base.copy()

    maximal_candidates = keep_only_max_candidates(base, formula)
    best = max(maximal_candidates, key=score_candidate)
    return best.copy()

def revise (base, formula, priority, source="new"):
    parsed = parse_formula(formula) if isinstance(formula, str) else formula
    contracted = contract(base, Not(parsed))
    return expand(contracted, parsed, priority, source)