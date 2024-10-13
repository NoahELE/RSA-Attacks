from sympy import (
    nextprime,
    isprime,
    continued_fraction_convergents,
    continued_fraction_iterator,
)
from random import getrandbits
from math import gcd


def generate_prime(bits):
    """
    Generates the prime given the number of bits
    """
    return nextprime(getrandbits(bits))


def generate_vulnerable_keypair(p, q):
    """
    Generates rsa key pair

    **p and q should have been checked for primality

    Returns the public and private key pair
    """

    n = p * q
    phi = (p - 1) * (q - 1)

    d_max = int(1 / 3 * (n**0.25))  # vulnerability for Wiener's attack to occur
    d = -1
    for i in range(2, d_max):
        if gcd(i, phi) == 1:
            d = i
            break
    if d == -1:
        raise ValueError("private key not found")

    e = pow(d, -1, phi)
    return ((e, n), (d, n))


def generate_low_public_exponent_scheme(prime_bits=1024):
    """
    Generates a vaible attack scenario for low public exponent attack
    the public exponent is set to three

    Returns the public and private key pair for the scheme
    """

    while True:
        try:
            p = generate_prime(prime_bits)
            q = generate_prime(prime_bits)
            assert isprime(p), "the generated number is not prime"
            assert isprime(q), "the generated number is not prime"
            keys = generate_vulnerable_keypair(p, q)
            break
        except ValueError:
            continue
    return keys


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


def wiener_attack(e, n):
    try:
        iter = continued_fraction_iterator(e / n)
        convergents_iter = continued_fraction_convergents(iter)
        for r in convergents_iter:
            # extract numerator and denominator
            k = r.p
            d = r.q

            if k == 0 or (e * d - 1) % k != 0:
                continue

            phi = (e * d - 1) // k
            b = n - phi + 1

            # check if x^2 - b*x + n = 0 has integer root
            discrim = b**2 - 4 * n
            if discrim >= 0:
                root = int(discrim**0.5)
                if root**2 == discrim and (b + root) % 2 == 0:
                    return d
        return None
    except Exception as e:
        return None


public_key, private_key = generate_low_public_exponent_scheme(10)

plaintext = 102

assert (
    plaintext < public_key[1]
), "plaintext should be smaller than modulus to gaurantee the attack scheme"

ciphertext = encrypt(plaintext, public_key)


print(f"Chosen public key: {public_key}")
print(f"Private key: {private_key}")
print(f"Plaintext: {plaintext}")
print(f"Encrypted plaintext: {ciphertext}")
print(f"Decrypted ciphertext: {decrypt(ciphertext, private_key)}")

# Perform Wiener's attack
recovered_private_key = wiener_attack(*public_key)
if recovered_private_key:
    print("Hacked!!!")
    print(f"Attack result: {recovered_private_key}")
else:
    print("Hacking failed")
