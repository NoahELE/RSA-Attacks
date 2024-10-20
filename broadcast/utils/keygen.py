from sympy import nextprime, isprime, gcd
from random import getrandbits
import gmpy2

gmpy2.get_context().precision = 2048


def generate_keys(prime_bits, e, num_receiver):
    """
    Generates keys for number of receivers based on prime_bits and public exponent e
    """

    keys = []
    for _ in range(num_receiver):
        # select p and q automatically and generate key pair
        while True:
            try:
                p = generate_prime(prime_bits)
                q = generate_prime(prime_bits)

                # check the primality of p and q
                assert isprime(p), "the generated number is not prime"
                assert isprime(q), "the generated number is not prime"

                # generate vulnerable key pair with small e
                key = generate_keypair(p, q, e)
                keys += [key]
                break
            except Exception:
                continue
    return keys


def encrypt_with_keys(plaintext: str, keys):
    int_plaintext = gmpy2.mpz("".join(f"{ord(char):03}" for char in plaintext))
    ciphertext_public_pair = []
    for pub, _ in keys:
        ciphertext = encrypt(int_plaintext, pub)
        ciphertext_public_pair += [(str(ciphertext), pub)]
    return ciphertext_public_pair


def totient(p, q):
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
