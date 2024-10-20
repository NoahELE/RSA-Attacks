from flask import Flask, jsonify
from utils import keygen
import os
import random

app = Flask(__name__)

prime_bits = 512
d_wiener_condition = True

# load environment variable if specified
if "NUM_BITS" in os.environ:
    try:
        prime_bits = int(os.environ["NUM_BITS"])
    except Exception:
        pass
if "WIENER" in os.environ:
    d_wiener_condition = True if os.environ["WIENER"].lower() == "y" else False


def generate_keys():
    # select p and q automatically and generate key pair
    while True:
        try:
            p = keygen.generate_prime(prime_bits)
            q = keygen.generate_prime(prime_bits)

            # check the primality of p and q
            assert keygen.isprime(p), "the generated number is not prime"
            assert keygen.isprime(q), "the generated number is not prime"

            # generate vulnerable key pair with small d
            w = int((1 / 3) * ((p * q) ** 0.25))
            if d_wiener_condition:
                d = random.randint(2, w)
            else:
                d = random.randint(w, keygen.totient(p, q))
            keys = keygen.generate_keypair_priv(p, q, d)
            return keys
        except Exception:
            continue


@app.route("/public_key", methods=["GET"])
def get_public_key():
    try:
        return jsonify(keys[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("----------Server----------")
    print("Starting server...")
    print(f"Number of bits: {prime_bits}")
    print(f"Wiener's vulnerable: {d_wiener_condition}")
    print("Genarating key pair...")
    keys = generate_keys()
    print(
        f"Key pair generated:\n public address: {keys[0]}\n private exponent: {keys[1][0]}"
    )
    print("--------------------------")
    app.run(port=5000)
