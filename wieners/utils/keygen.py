from sympy import nextprime, isprime, gcd
from random import getrandbits, randint


def generate_keys(prime_bits, d_wiener_condition):
    """
    Generates keys based on number of bits of p and q and whether the keys should be Wiener's vulnerable
    """

    # select p and q automatically and generate key pair
    while True:
        try:
            p = generate_prime(prime_bits)
            q = generate_prime(prime_bits)

            # check the primality of p and q
            assert isprime(p), "the generated number is not prime"
            assert isprime(q), "the generated number is not prime"

            # generate vulnerable key pair with small d
            w = int((1 / 3) * ((p * q) ** 0.25))
            if d_wiener_condition:
                d = randint(2, w)
            else:
                d = randint(w, totient(p, q))
            keys = generate_keypair_priv(p, q, d)
            return keys
        except Exception:
            continue


def totient(p, q):
    """Computes phi"""
    return (p - 1) * (q - 1)


def generate_prime(bits):
    """
    Generates the prime given the number of bits
    """
    return nextprime(getrandbits(bits))


def generate_keypair(p, q, e):
    """
    Generates rsa key pair given public exponent e

    **p and q should have been checked for primality

    Returns the public and private key pair
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return ((e, n), (d, n))


def generate_keypair_priv(p, q, d):
    """
    Generates rsa key pair given private exponent d

    **p and q should have been checked for primality

    Returns the public and private key pair
    """
    pub, priv = generate_keypair(p, q, d)
    return (priv, pub)


def encrypt(plaintext, key):
    """
    Encrypts the plaintext with the public keys

    Returns the ciphertext
    """
    e, n = key
    return pow(plaintext, e, n)


def decrypt(ciphertext, key):
    """
    Dencrypts the ciphertext with the private keys

    Returns the plaintext
    """
    d, n = key
    return pow(ciphertext, d, n)
