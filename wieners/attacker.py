import requests
import os
import func_timeout
import gmpy2
from gmpy2 import mpz, isqrt
import time

gmpy2.get_context().precision = 2048


TIMEOUT = 10  # defualt timeout for attacking (in second)

if "TIMEOUT" in os.environ:
    try:
        TIMEOUT = int(os.environ["TIMEOUT"])
    except Exception:
        pass


def continued_fraction_iter(n, d):
    """
    Generator for quotient of numerator n and denominator d
    """
    while d:
        q = n // d
        yield q
        n, d = d, n - q * d  # new numerator and new denominator


def get_convergents(iter):
    """
    Iteratively recovers numerator and denominator from continued fraction iterator
    """
    # previous values
    n_0 = mpz(0)
    d_0 = mpz(1)

    # current values
    n_1 = mpz(1)
    d_1 = mpz(0)

    for q in iter:
        n_0, n_1 = n_1, q * n_1 + n_0
        d_0, d_1 = d_1, q * d_1 + d_0
        yield (n_1, d_1)


def wiener_attack(e, n):
    e = mpz(str(e))  # convert int to str for gmpy2 compatibility
    n = mpz(str(n))
    try:
        iter = continued_fraction_iter(e, n)
        convergents = get_convergents(iter)
        for k, d in convergents:
            if k == 0 or (e * d - 1) % k != 0:
                continue

            phi = (e * d - 1) // k
            b = n - phi + 1

            # check if x^2 - b*x + n = 0 has integer root
            discrim = b**2 - 4 * n
            if discrim >= 0:
                root = isqrt(discrim)
                if root * root == discrim and ((b + root) % 2 == 0):
                    return int(d)
        return None
    except Exception as e:
        return None


SERVER_URL = "http://localhost:5000"


def get_public_key():
    try:
        response = requests.get(f"{SERVER_URL}/public_key")
        if response.ok:
            return response.json()
        return None
    except Exception:
        return None


if __name__ == "__main__":
    print("----------Attacker----------")

    patient = 3
    public_key = None
    while patient != 0:
        public_key = get_public_key()
        if not public_key:
            print("Waiting for server...for 10 more sec")
            time.sleep(10)
            patient -= 1
        else:
            break
    if not public_key:
        print("No more patience. Server seems to be busy generating keys.")
        raise Exception("Error: fail to get public key")

    e, n = public_key
    print(f"Public key obtained: (e={e}, n={n})\n")

    print(f"Running attack...with timeout {TIMEOUT}s")

    try:
        priv_key_d = func_timeout.func_timeout(TIMEOUT, wiener_attack, args=(e, n))
        if priv_key_d:
            print(f"Private key found: d={priv_key_d}")
        else:
            print("Failed to find the private key.")
    except func_timeout.FunctionTimedOut:
        print("Timeout: failed to find the private key.")
    except Exception:
        print("Exception: failed to find the private key.")
    print("--------------------------")
