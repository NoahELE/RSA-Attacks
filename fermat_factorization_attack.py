import math

from common import RSAKeyPair


def rsa_keygen() -> RSAKeyPair:
    """Generate a RSA key pair with 2 close prime numbers."""
    p = 65537
    q = 65539
    n = p * q
    e = 7
    d = pow(e, -1, (p - 1) * (q - 1))
    return RSAKeyPair(n, e, p, q, d)


def fermat_factorization(n: int) -> tuple[int, int]:
    """Factorize n using Fermat's factorization method."""
    a = math.ceil(math.sqrt(n))
    b2 = a**2 - n
    while not math.sqrt(b2).is_integer():
        a += 1
        b2 = a**2 - n
    return int(a - math.sqrt(b2)), int(a + math.sqrt(b2))


def fermat_factorization_attack(c: int, n: int, e: int) -> int:
    """Recover the plaintext m from the ciphertext c."""
    p, q = fermat_factorization(n)
    d = pow(e, -1, (p - 1) * (q - 1))
    m_recovered = pow(c, d, n)
    return m_recovered


if __name__ == "__main__":
    # 2 close prime numbers
    kp = rsa_keygen()

    m = 103
    c = pow(m, kp.e, kp.n)

    print(f"Plaintext: {m}")
    print(f"Ciphertext: {c}")

    # Fermat factorization attack
    m_recovered = fermat_factorization_attack(c, kp.n, kp.e)
    print(f"Recovered plaintext: {m_recovered}")
