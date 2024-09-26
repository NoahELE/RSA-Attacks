from sympy import nextprime, isprime
from random import getrandbits


def generate_prime(bits):
    """
    Generates the prime given the number of bits
    """
    return nextprime(getrandbits(bits))


def generate_keypair(p, q, e):
    """
    Generates rsa key pair

    **p and q should have been checked for primality

    Returns the public and private key pair
    """

    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return ((e, n), (d, n))


def generate_low_public_exponent_scheme(prime_bits=1024):
    """
    Generates a vaible attack scenario for low public exponent attack
    the public exponent is set to three

    Returns the public and private key pair for the scheme
    """

    # We use relatively small public exponent for demonstration
    e = 3

    while True:
        try:
            p = generate_prime(prime_bits)
            q = generate_prime(prime_bits)
            assert isprime(p), "the generated number is not prime"
            assert isprime(q), "the generated number is not prime"
            keys = generate_keypair(p, q, e)
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
    if plaintext**3 < n:
        print("Note: Cubic root attack is viable")
    return pow(plaintext, e, n)


def decrypt(ciphertext, key):
    """
    Dencrypts the ciphertext with the private keys

    Returns the plaintext
    """
    d, n = key
    return pow(ciphertext, d, n)


def crt(*cipherpair):
    try:
        n = 1
        for _, pub in cipherpair:
            _, n_i = pub
            n *= n_i

        re = 0
        for c, pub in cipherpair:
            _, n_i = pub
            n_c = n // n_i
            re += c * n_c * pow(n_c, -1, n_i) % n
        return re % n
    except ValueError:
        raise ValueError("Inverse modulus not found in CRT.")


def cube_root(n):
    return round(n ** (1.0 / 3))


public_key1, private_key1 = generate_low_public_exponent_scheme(10)
public_key2, private_key2 = generate_low_public_exponent_scheme(10)
public_key3, private_key3 = generate_low_public_exponent_scheme(10)

# In order for the attack to occur, we should have a relatively small plaintext
# that is, the plaintext should be shorter than the prime
plaintext = 102

assert (
    plaintext < public_key1[1]
), "plaintext should be smaller than modulus to gaurantee the attack scheme"
assert (
    plaintext < public_key2[1]
), "plaintext should be smaller than modulus to gaurantee the attack scheme"
assert (
    plaintext < public_key3[1]
), "plaintext should be smaller than modulus to gaurantee the attack scheme"

ciphertext1 = encrypt(plaintext, public_key1)
ciphertext2 = encrypt(plaintext, public_key2)
ciphertext3 = encrypt(plaintext, public_key3)

cipher = crt(
    (ciphertext1, public_key1), (ciphertext2, public_key2), (ciphertext3, public_key3)
)

print(f"Plaintext: {plaintext}")
print(f"Encrypted plaintext: {ciphertext1}")
print(f"Decrypted ciphertext: {decrypt(ciphertext1, private_key1)}")

# Perform the low public exponent attack
recovered_plaintext = cube_root(cipher)
print(f"Attack result: {recovered_plaintext}")

if plaintext == recovered_plaintext:
    print("Hacked!!!")
else:
    print("Hacking failed")
