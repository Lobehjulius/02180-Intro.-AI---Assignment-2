* Phase 1
    - parse formulas
    - store a belief base
    - check entailment with resolution
* Phase 2
    - implement expansion
    - implement contraction with priority
* Phase 3
    - define revision using Levi identity
    - add tests


    logic for the parser
parse_formula()
  → parse_biconditional()
    → parse_implication()
      → parse_disjunction()
        → parse_conjunction()
          → parse_negation()
            → parse_primary()