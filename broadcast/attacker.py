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


SERVER_URL = "http://localhost:5000"


def get_ciphertext_public_key():
    try:
        response = requests.get(f"{SERVER_URL}/ciphertext_public_key")
        if response.ok:
            return response.json()["ciphertext_public"]
        return None
    except Exception:
        return None


if __name__ == "__main__":
    print("----------Attacker----------")

    patient = 3
    ciphertext_public_pairs = None
    while patient != 0:
        ciphertext_public_pairs = get_ciphertext_public_key()
        if not ciphertext_public_pairs:
            print("Waiting for server...for 10 more sec")
            time.sleep(10)
            patient -= 1
        else:
            break
    if not ciphertext_public_pairs:
        print("No more patience. Server seems to be busy generating keys.")
        raise Exception("Error: fail to get public key")

    print("Messages (ciphertext) intercepted")

    print(f"Running attack...with timeout {TIMEOUT}s")

    try:
        cipher = func_timeout.func_timeout(
            TIMEOUT, crt, args=(ciphertext_public_pairs,)
        )
        e = ciphertext_public_pairs[0][1][0]
        if cipher:
            byte_recovered_plaintext = cipher ** (1.0 / e)
            print(f"Recovered plaintext: {byte_recovered_plaintext.decode()}")
        else:
            print("Failed to recover the plaintext.")
    except func_timeout.FunctionTimedOut:
        print("Timeout: failed to recover the plaintext.")
    except Exception:
        print("Exception: failed to recover the plaintext.")
    print("--------------------------")
