from typing import Callable

import sympy as sp
from cryptography.hazmat.primitives.asymmetric import rsa

from common import RSAKeyPair


def rsa_keygen(bits: int = 1024) -> RSAKeyPair:
    """Generate a RSA key pair."""
    e = 3
    private_key = rsa.generate_private_key(public_exponent=e, key_size=bits)
    return RSAKeyPair(
        n=private_key.public_key().public_numbers().n,
        e=e,
        p=private_key.private_numbers().p,
        q=private_key.private_numbers().q,
        d=private_key.private_numbers().d,
    )


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
    kp = rsa_keygen()

    m = 100232
    c = encrypt(m, kp.n, kp.e)

    print(f"Plaintext: {m}")
    print(f"Ciphertext: {c}")

    # Chosen ciphertext attack
    m_recovered = chosen_ciphertext_attack(
        c, kp.n, kp.e, lambda c: decrypt(c, kp.n, kp.d)
    )
    print(f"Recovered plaintext: {m_recovered}")
