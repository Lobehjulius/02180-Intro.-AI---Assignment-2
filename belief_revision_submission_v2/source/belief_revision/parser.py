from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from .formula import And, Const, Formula, Iff, Implies, Not, Or, Var

_TOKEN_RE = re.compile(
    r"\s*(<->|->|[()~!&|]|and\b|or\b|not\b|TRUE\b|FALSE\b|true\b|false\b|[A-Za-z][A-Za-z0-9_]*|\S)"
)


class ParseError(ValueError):
    pass


@dataclass
class _TokenStream:
    tokens: List[str]
    index: int = 0

    def peek(self) -> str | None:
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]

    def consume(self, expected: str | None = None) -> str:
        token = self.peek()
        if token is None:
            raise ParseError("Unexpected end of input")
        if expected is not None and token != expected:
            raise ParseError(f"Expected '{expected}' but found '{token}'")
        self.index += 1
        return token


def tokenize(text: str) -> List[str]:
    tokens: List[str] = []
    position = 0
    while position < len(text):
        match = _TOKEN_RE.match(text, position)
        if not match:
            raise ParseError(f"Could not tokenize formula near: {text[position:]}")
        token = match.group(1)
        position = match.end()
        lowered = token.lower()
        if lowered == "and":
            tokens.append("&")
        elif lowered == "or":
            tokens.append("|")
        elif lowered == "not" or token == "!":
            tokens.append("~")
        elif lowered == "true":
            tokens.append("TRUE")
        elif lowered == "false":
            tokens.append("FALSE")
        elif token in {"<->", "->", "(", ")", "~", "&", "|"}:
            tokens.append(token)
        elif re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", token):
            tokens.append(token)
        else:
            raise ParseError(f"Unexpected token '{token}'")
    return tokens


class _Parser:
    def __init__(self, text: str):
        self.stream = _TokenStream(tokenize(text))

    def parse(self) -> Formula:
        formula = self.parse_iff()
        if self.stream.peek() is not None:
            raise ParseError(f"Unexpected trailing token '{self.stream.peek()}'")
        return formula

    def parse_iff(self) -> Formula:
        left = self.parse_implies()
        while self.stream.peek() == "<->":
            self.stream.consume("<->")
            right = self.parse_implies()
            left = Iff(left, right)
        return left

    def parse_implies(self) -> Formula:
        left = self.parse_or()
        if self.stream.peek() == "->":
            self.stream.consume("->")
            right = self.parse_implies()
            return Implies(left, right)
        return left

    def parse_or(self) -> Formula:
        left = self.parse_and()
        while self.stream.peek() == "|":
            self.stream.consume("|")
            right = self.parse_and()
            left = Or(left, right)
        return left

    def parse_and(self) -> Formula:
        left = self.parse_unary()
        while self.stream.peek() == "&":
            self.stream.consume("&")
            right = self.parse_unary()
            left = And(left, right)
        return left

    def parse_unary(self) -> Formula:
        token = self.stream.peek()
        if token is None:
            raise ParseError("Unexpected end of input")
        if token == "~":
            self.stream.consume("~")
            return Not(self.parse_unary())
        if token == "(":
            self.stream.consume("(")
            inside = self.parse_iff()
            self.stream.consume(")")
            return inside
        if token == "TRUE":
            self.stream.consume("TRUE")
            return Const(True)
        if token == "FALSE":
            self.stream.consume("FALSE")
            return Const(False)
        self.stream.consume()
        return Var(token)


def parse_formula(text: str) -> Formula:
    return _Parser(text).parse()
