from .vector import Vector


def gram_schmidt(vectors: list[Vector]) -> list[Vector]:
    output = []
    for v in vectors:
        next_e = sum([-e.scaled(v * e) for e in output], start=v)
        output.append(next_e.normalized())
    return output
