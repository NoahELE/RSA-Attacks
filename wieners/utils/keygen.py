from sympy import nextprime, isprime, gcd
from random import getrandbits


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
