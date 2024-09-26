import sympy as sp
from cryptography.hazmat.primitives.asymmetric import rsa

from common import RSAKeyPair


def rsa_keygen(bits: int = 1024) -> tuple[RSAKeyPair, RSAKeyPair, RSAKeyPair]:
    """Generate 3 RSA key pairs with the same small public exponent e = 3."""
    e = 3

    private_key1 = rsa.generate_private_key(public_exponent=e, key_size=bits)
    private_key2 = rsa.generate_private_key(public_exponent=e, key_size=bits)
    private_key3 = rsa.generate_private_key(public_exponent=e, key_size=bits)

    if (
        private_key1.public_key().public_numbers().n
        == private_key2.public_key().public_numbers().n
    ):
        raise ValueError("n1 and n2 are the same")
    if (
        private_key1.public_key().public_numbers().n
        == private_key3.public_key().public_numbers().n
    ):
        raise ValueError("n1 and n3 are the same")
    if (
        private_key2.public_key().public_numbers().n
        == private_key3.public_key().public_numbers().n
    ):
        raise ValueError("n2 and n3 are the same")

    return (
        RSAKeyPair(
            n=private_key1.public_key().public_numbers().n,
            e=e,
            p=private_key1.private_numbers().p,
            q=private_key1.private_numbers().q,
            d=private_key1.private_numbers().d,
        ),
        RSAKeyPair(
            n=private_key2.public_key().public_numbers().n,
            e=e,
            p=private_key2.private_numbers().p,
            q=private_key2.private_numbers().q,
            d=private_key2.private_numbers().d,
        ),
        RSAKeyPair(
            n=private_key3.public_key().public_numbers().n,
            e=e,
            p=private_key3.private_numbers().p,
            q=private_key3.private_numbers().q,
            d=private_key3.private_numbers().d,
        ),
    )


def chinese_remainder_theorem(
    n1: int, n2: int, n3: int, a1: int, a2: int, a3: int
) -> int:
    """Solve the system of congruences using the Chinese Remainder Theorem."""
    n = n1 * n2 * n3
    m1 = n2 * n3
    m2 = n1 * n3
    m3 = n1 * n2
    y1 = pow(m1, -1, n1)
    y2 = pow(m2, -1, n2)
    y3 = pow(m3, -1, n3)
    x = (a1 * m1 * y1 + a2 * m2 * y2 + a3 * m3 * y3) % n
    return x


def hastad_broadcast_attack(
    c1: int, c2: int, c3: int, kp1: RSAKeyPair, kp2: RSAKeyPair, kp3: RSAKeyPair
) -> int:
    """
    Recover the plaintext m from 3 RSA ciphertexts given they share the same
    small public exponent e = 3.
    """
    x = chinese_remainder_theorem(kp1.n, kp2.n, kp3.n, c1, c2, c3)
    m_recovered = sp.cbrt(x)
    return m_recovered


if __name__ == "__main__":
    kp1, kp2, kp3 = rsa_keygen()

    m = 100232
    c1 = pow(m, kp1.e, kp1.n)
    c2 = pow(m, kp2.e, kp2.n)
    c3 = pow(m, kp3.e, kp3.n)

    print(f"Plaintext: {m}")
    print(f"Ciphertext 1: {c1}")
    print(f"Ciphertext 2: {c2}")
    print(f"Ciphertext 3: {c3}")

    # Hastad broadcast attack
    m_recovered = hastad_broadcast_attack(c1, c2, c3, kp1, kp2, kp3)
    print(f"Recovered plaintext: {m_recovered}")
