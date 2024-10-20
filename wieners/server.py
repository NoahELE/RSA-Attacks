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
    keys = keygen.generate_keys(prime_bits, d_wiener_condition)
    print(
        f"Key pair generated:\n public address: {keys[0]}\n private exponent: {keys[1][0]}"
    )
    print("--------------------------")
    app.run(port=5000)
