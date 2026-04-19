from dataclasses  import dataclass

@dataclass(frozen=True)
class Atom:
    name: str
    def __str__(self):
        return self.name

@dataclass(frozen=True)
class Not:
    child: object
    def __str__(self):
        return f"~{self.child}"

@dataclass(frozen=True)
class And:
    left: object
    right: object
    def __str__(self):
        return f"{self.left} & {self.right}"

@dataclass(frozen=True)
class Or:
    left: object
    right: object
    def __str__(self):
        return f"{self.left} | {self.right}"

@dataclass(frozen=True)
class Imp:
    left: object
    right: object
    def __str__(self):
        return f"{self.left} -> {self.right}"

@dataclass(frozen=True)
class Iff:
    left: object
    right: object
    def __str__(self):
        return f"{self.left} <-> {self.right}"
