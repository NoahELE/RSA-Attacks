import requests
from Crypto.PublicKey import RSA

from schemes import wiener

SERVER_URL = "http://server:5000"  # to be changed to environment var


def get_public_key():
    response = requests.get(f"{SERVER_URL}/public_key")
    return RSA.import_key(response.content)


if __name__ == "__main__":
    public_key = get_public_key()
    e = public_key.e
    n = public_key.n
    print(f"Public key obtained: (e={e}, n={n})\n")

    priv_key_d = wiener.wiener_attack(e, n)
    if priv_key_d:
        print(f"Private key found: d={priv_key_d}\n")
    else:
        print("Wiener's attack failed to find the private key.")
