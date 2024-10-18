import gmpy2
from sympy import gcd


def pollard_factorization(n: int, bound: int = 1024) -> int | None:
    a = 2
    for j in range(2, bound):
        a = pow(a, j, n)
        p = gcd(a - 1, n)
        if 1 < p < n:
            return int(p)
    return None


def pollard_attack(n: int, e: int) -> int | None:
    p = pollard_factorization(n)
    if p is None:
        return None
    q = n // p
    print(f"p: {p}, q: {q}")
    d = pow(e, -1, (p - 1) * (q - 1))
    return d


p = gmpy2.next_prime(2**22)
q = gmpy2.next_prime(p)
n = p * q
d = pollard_attack(n, 37)
print(f"n = {n} d = {d}")
