import requests
import os
import func_timeout
import gmpy2
import time
from utils import attack

gmpy2.get_context().precision = 2048


TIMEOUT = 10  # defualt timeout for attacking (in second)

if "TIMEOUT" in os.environ:
    try:
        TIMEOUT = int(os.environ["TIMEOUT"])
    except Exception:
        pass


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
        cipher, key_info = func_timeout.func_timeout(
            TIMEOUT, attack.crt, args=(*ciphertext_public_pairs,)
        )
        e = ciphertext_public_pairs[0][1][0]
        ciphertext0 = ciphertext_public_pairs[0][0]

        if key_info:
            print("Common divisor found in moduli. Decrypt message directly.")

            recovered_int = attack.decrypt_message(key_info, ciphertext0)
            print(
                f"Recovered int plaintext: {attack.convert_to_plaintext(gmpy2.mpz(str(recovered_int)))}"
            )
        elif cipher:
            recovered_mpz = int(cipher ** (1.0 / gmpy2.mpz(e)))
            print(
                f"Recovered int plaintext: {attack.convert_to_plaintext(recovered_mpz)}"
            )
        else:
            print("Failed to recover the plaintext.")
    except func_timeout.FunctionTimedOut:
        print("Timeout: failed to recover the plaintext.")
    except Exception as e:
        print(e)
        print("Exception: failed to recover the plaintext.")
    print("--------------------------")
