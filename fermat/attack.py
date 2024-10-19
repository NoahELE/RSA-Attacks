import numpy as np
import requests


def fermat_factorization(n: int) -> tuple[int, int]:
    """Factorize n using Fermat's factorization method."""
    a = np.ceil(np.sqrt(n))
    b2 = a**2 - n
    while not np.sqrt(b2).is_integer():
        a += 1
        b2 = a**2 - n
    return int(a - np.sqrt(b2)), int(a + np.sqrt(b2))


def fermat_attack(n: int, e: int) -> int:
    """Recover the plaintext m from the ciphertext c."""
    p, q = fermat_factorization(n)
    d = pow(e, -1, (p - 1) * (q - 1))
    return d


print("--- Fermat's Factorization Attack ---")

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

d = fermat_attack(n, e)
print(f"d: {d}")

m_decrypted = c**d % n
print(f"m_decrypted: {m_decrypted}")
