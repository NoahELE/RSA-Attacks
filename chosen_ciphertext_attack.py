from typing import Callable

import sympy as sp


def rsa_keygen(bits: int = 512) -> tuple[int, int, int, int, int]:
    """Generate RSA modulus n = p * q with small public exponent e."""
    p = sp.randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2))
    q = sp.randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2))
    n = p * q
    e = sp.randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2))
    d = sp.mod_inverse(e, (p - 1) * (q - 1))
    return n, e, p, q, d


def encrypt(m: int, n: int, e: int) -> int:
    """Encrypt message m with public key (n, e)."""
    return pow(m, e, n)


def decrypt(c: int, n: int, d: int) -> int:
    """Decrypt ciphertext c with private key (n, d)."""
    return pow(c, d, n)


def chosen_ciphertext_attack(
    c: int, n: int, e: int, decrypt: Callable[[int], int]
) -> int:
    """Recover the plaintext m from the ciphertext c."""
    r = 2
    m1 = decrypt(encrypt(r, n, e) * c % n)
    m_recovered = m1 * sp.mod_inverse(r, n) % n
    return m_recovered


if __name__ == "__main__":
    n, e, p, q, d = rsa_keygen()
    print(f"Public key: n = {n} e = {e}")
    print(f"Private key: p = {p} q = {q} d = {d}")

    m = 100232
    c = encrypt(m, n, e)

    print(f"Plaintext: {m}")
    print(f"Ciphertext: {c}")

    # Chosen ciphertext attack
    m_recovered = chosen_ciphertext_attack(c, n, e, lambda c: decrypt(c, n, d))
    print(f"Recovered plaintext: {m_recovered}")
