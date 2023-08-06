from dataclasses import dataclass
from typing import Callable, Union

import sympy

Constant = Union[sympy.Mul, float, int]


@dataclass
class BasisVector:
    name: str

    def __str__(self):
        return self.name


@dataclass
class VectorSpace:
    basis_vectors: list[BasisVector]
    inner_product: Callable[["Vector", "Vector"], Constant]


class Vector:
    components: list[sympy.Mul]
    space: VectorSpace

    def __init__(self, components: list[Constant], space: "VectorSpace"):
        self.components = list(map(sympy.Mul, components))
        self.space = space

    def __str__(self):
        return " + ".join(f"({comp}){vec}" for comp, vec in zip(self.components, self.space.basis_vectors))

    def __mul__(self, other: "Vector") -> sympy.Mul:
        if self.space is not other.space:
            raise ValueError("vectors must be in the same space")
        return sympy.Mul(self.space.inner_product(self, other))

    def __add__(self, other: "Vector") -> "Vector":
        if self.space is not other.space:
            raise ValueError("vectors must be in the same space")
        return Vector([c1 + c2 for c1, c2 in zip(self.components, other.components)], self.space)

    def __neg__(self):
        return self.scaled(-1)

    def __sub__(self, other: "Vector") -> "Vector":
        return self + -other

    def norm(self) -> sympy.Expr:
        return sympy.sqrt(self * self)

    def scaled(self, constant: Constant) -> "Vector":
        return Vector([c * sympy.Mul(constant) for c in self.components], self.space)

    def normalized(self) -> "Vector":
        return self.scaled(1 / self.norm())
