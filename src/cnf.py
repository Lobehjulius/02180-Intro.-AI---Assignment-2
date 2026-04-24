from node import And, Atom, Iff, Imp, Not, Or


def eliminate_iff(expr):
    """
    Rewrite biconditionals:
        A <-> B  =>  (A -> B) & (B -> A)
    """
    if isinstance(expr, Atom):
        return expr
    if isinstance(expr, Not):
        return Not(eliminate_iff(expr.child))
    if isinstance(expr, And):
        return And(eliminate_iff(expr.left), eliminate_iff(expr.right))
    if isinstance(expr, Or):
        return Or(eliminate_iff(expr.left), eliminate_iff(expr.right))
    if isinstance(expr, Imp):
        return Imp(eliminate_iff(expr.left), eliminate_iff(expr.right))
    if isinstance(expr, Iff):
        left = eliminate_iff(expr.left)
        right = eliminate_iff(expr.right)
        return And(Imp(left, right), Imp(right, left))
    raise TypeError(f"Unsupported expression type: {type(expr)!r}")


def eliminate_imp(expr):
    """
    Rewrite implications:
        A -> B  =>  ~A | B
    """
    if isinstance(expr, Atom):
        return expr
    if isinstance(expr, Not):
        return Not(eliminate_imp(expr.child))
    if isinstance(expr, And):
        return And(eliminate_imp(expr.left), eliminate_imp(expr.right))
    if isinstance(expr, Or):
        return Or(eliminate_imp(expr.left), eliminate_imp(expr.right))
    if isinstance(expr, Imp):
        left = eliminate_imp(expr.left)
        right = eliminate_imp(expr.right)
        return Or(Not(left), right)
    if isinstance(expr, Iff):
        return eliminate_imp(eliminate_iff(expr))
    raise TypeError(f"Unsupported expression type: {type(expr)!r}")


def push_negations(expr):
    """
    Push negations inward using De Morgan's laws and double negation elimination:
        ~(A & B)  =>  ~A | ~B
        ~(A | B)  =>  ~A & ~B
        ~~A       =>  A
    """
    if isinstance(expr, Atom):
        return expr

    if isinstance(expr, Not):
        child = expr.child

        if isinstance(child, Atom):
            return expr

        if isinstance(child, Not):
            return push_negations(child.child)

        if isinstance(child, And):
            return Or(
                push_negations(Not(child.left)),
                push_negations(Not(child.right)),
            )

        if isinstance(child, Or):
            return And(
                push_negations(Not(child.left)),
                push_negations(Not(child.right)),
            )

        if isinstance(child, Imp) or isinstance(child, Iff):
            return push_negations(Not(eliminate_imp(eliminate_iff(child))))

        return Not(push_negations(child))

    if isinstance(expr, And):
        return And(push_negations(expr.left), push_negations(expr.right))

    if isinstance(expr, Or):
        return Or(push_negations(expr.left), push_negations(expr.right))

    if isinstance(expr, Imp):
        return push_negations(eliminate_imp(expr))

    if isinstance(expr, Iff):
        return push_negations(eliminate_imp(eliminate_iff(expr)))

    raise TypeError(f"Unsupported expression type: {type(expr)!r}")


def distribute_or_over_and(expr):
    """
    Distribute OR over AND:
        A | (B & C)  =>  (A | B) & (A | C)
        (A & B) | C  =>  (A | C) & (B | C)
    """
    if isinstance(expr, Atom) or (
        isinstance(expr, Not) and isinstance(expr.child, Atom)
    ):
        return expr

    if isinstance(expr, Not):
        return expr

    if isinstance(expr, And):
        left = distribute_or_over_and(expr.left)
        right = distribute_or_over_and(expr.right)
        return And(left, right)

    if isinstance(expr, Or):
        left = distribute_or_over_and(expr.left)
        right = distribute_or_over_and(expr.right)

        if isinstance(left, And):
            return And(
                distribute_or_over_and(Or(left.left, right)),
                distribute_or_over_and(Or(left.right, right)),
            )

        if isinstance(right, And):
            return And(
                distribute_or_over_and(Or(left, right.left)),
                distribute_or_over_and(Or(left, right.right)),
            )

        return Or(left, right)

    raise TypeError(f"Unsupported expression type: {type(expr)!r}")


def to_cnf(expr):
    """
    Convert expression to CNF as an AST.

    Pipeline:
        1. Eliminate biconditionals
        2. Eliminate implications
        3. Push negations inward
        4. Distribute OR over AND
    """
    expr = eliminate_iff(expr)
    expr = eliminate_imp(expr)
    expr = push_negations(expr)
    expr = distribute_or_over_and(expr)
    return expr


def _literal_to_string(expr) -> str:
    """
    Convert a literal AST node to a string literal.
    """
    if isinstance(expr, Atom):
        return expr.name
    if isinstance(expr, Not) and isinstance(expr.child, Atom):
        return f"~{expr.child.name}"
    raise ValueError(f"Not a literal: {expr!r}")


def is_literal(expr) -> bool:
    """
    Check whether expr is a literal:
        p
        ~p
    """
    return isinstance(expr, Atom) or (
        isinstance(expr, Not) and isinstance(expr.child, Atom)
    )


def _collect_literals(expr) -> set[str]:
    """
    Flatten a disjunction into a set of literal strings.
    """
    if isinstance(expr, Or):
        return _collect_literals(expr.left) | _collect_literals(expr.right)

    if is_literal(expr):
        return {_literal_to_string(expr)}

    raise ValueError(f"Not a literal or disjunction: {expr!r}")


def cnf_to_clauses(expr) -> set[frozenset[str]]:
    """
    Convert a formula to a set of CNF clauses.

    Each clause is a frozenset of literal strings, for example:
        {"p", "~q"}

    The whole CNF is a set of such clauses.
    """
    expr = to_cnf(expr)

    if is_literal(expr):
        return {frozenset({_literal_to_string(expr)})}

    if isinstance(expr, Or):
        return {frozenset(_collect_literals(expr))}

    if isinstance(expr, And):
        left_clauses = cnf_to_clauses(expr.left)
        right_clauses = cnf_to_clauses(expr.right)
        return left_clauses | right_clauses

    raise ValueError(f"Expression is not in CNF form: {expr!r}")


def is_clause(expr) -> bool:
    """
    Check whether expr is a clause in CNF form:
        p
        ~p
        p | q | ~r
    """
    if is_literal(expr):
        return True
    if isinstance(expr, Or):
        return is_clause(expr.left) and is_clause(expr.right)
    return False


def is_cnf(expr) -> bool:
    """
    Check whether expr is in CNF form.
    """
    expr = to_cnf(expr)

    if is_clause(expr):
        return True

    if isinstance(expr, And):
        return is_cnf(expr.left) and is_cnf(expr.right)

    return False


if __name__ == "__main__":
    from parser import parse_formula

    examples = [
        "p",
        "~p",
        "p & q",
        "p | q & r",
        "~(p | q) -> r",
        "p <-> (q -> ~r)",
    ]

    for text in examples:
        formula = parse_formula(text)
        cnf_formula = to_cnf(formula)
        clauses = cnf_to_clauses(formula)
        print(f"{text:20} => {cnf_formula}")
        print(f"{'':20}    clauses: {clauses}")