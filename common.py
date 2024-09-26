from dataclasses import dataclass


@dataclass
class RSAKeyPair:
    n: int
    e: int
    p: int
    q: int
    d: int

    def public_key(self) -> tuple[int, int]:
        return self.n, self.e

    def private_key(self) -> tuple[int, int, int]:
        return self.p, self.q, self.d
