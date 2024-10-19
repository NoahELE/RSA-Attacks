import time

import requests
from numpy import gcd


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


time.sleep(5)  # wait for the server to start

SERVER_URL = "http://localhost:5000"

m = 42

c = requests.post(
    f"{SERVER_URL}/encrypt",
    json={"m": m},
).json()["c"]
print(f"c: {c}")

public_key = requests.get(f"{SERVER_URL}/public_key").json()
n = public_key["n"]
e = public_key["e"]
print(f"n: {n}")
print(f"e: {e}")

d = pollard_attack(n, e)
print(f"d: {d}")

m_decrypted = c**d % n
print(f"m_decrypted: {m_decrypted}")
