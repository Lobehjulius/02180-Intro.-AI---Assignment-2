from node import Atom, Not, And, Or, Imp, Iff
import re


TOKEN_RE = re.compile(r"\s*(<->|->|[()~&|]|[A-Za-z0-9_]*)")

def tokenize(text: str) -> list[str]:
    pos = 0
    tokens = []

    while pos <len(text):
        match = TOKEN_RE.match(text,pos)
        if not match:
            raise SyntaxError(f"Unexpected character at position {pos}: {text[pos]!r}")
        token = match.group(1)
        if token: 
            tokens.append(token)
        pos = match.end()
    return tokens


class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> str:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self, expected = None):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        if expected is not None and token != expected:
            raise SyntaxError(f"Expected {expected!r} but got {token!r}")
        self.pos += 1
        return token
    
    def parse(self):
        result = self.parse_iff()
        if self.peek() is not None:
            raise SyntaxError(f"unexpected token: {self.peek()}")
        return result

    def parse_iff(self):
        left = self.parse_imp()
        while self.peek() == "<->":
            self.consume("<->")
            right = self.parse_imp()
            left = Iff(left, right)
        return left
        
    def parse_imp(self):
        left = self.parse_or()
        if self.peek() == "->":
            self.consume("->")
            right = self.parse_imp()
            return Imp(left, right)
        return left
    
    def parse_or(self):
        left = self.parse_and()
        while self.peek() == "|":
            self.consume("|")
            right = self.parse_and()
            left =  Or(left, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.peek() == "&":
            self.consume("&")
            right = self.parse_not()
            left = And(left, right)
        return left
    
    def parse_not(self):
        if self.peek() == "~":
            self.consume("~")
            return Not(self.parse_not())
        return self.parse_atom()
    
    def parse_atom(self):
        token = self.peek()

        if token == "(":
            self.consume("(")
            expr = self.parse_iff()
            self.consume(")")
            return expr
        
        if token is not None and re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", token):
            self.consume()
            return Atom(token)
        
        raise SyntaxError(f"Expected atom or '(', got {token}")
        



def parse_formula(text: str):
    return Parser(tokenize(text)).parse()
    

if __name__ == "__main__":
    examples = [
        "p",
        "~p",
        "p & q",
        "p | q & r",
        "~(p | q) -> r",
        "p <-> (q -> ~r)"
    ]
    
    for expr in examples:
        try:
            result = parse_formula(expr)
            print(f"{expr:20} → {result}")
        except SyntaxError as e:
            print(f"{expr:20} → ERROR: {e}")
