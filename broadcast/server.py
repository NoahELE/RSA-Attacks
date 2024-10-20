from flask import Flask, jsonify
from utils import keygen
import os

app = Flask(__name__)

PRIME_BITS = 512  # constant
e = 3
receiver = 3
plaintext = "welcome to broadcast attack simulation."
random_pad = False

# load environment variable if specified
if "PUB_EXP" in os.environ:
    try:
        e = int(os.environ["PUB_EXP"])
    except Exception:
        pass
if "NUM_RECEIVER" in os.environ:
    try:
        receiver = int(os.environ["NUM_RECEIVER"])
    except Exception:
        pass
if "TEXT" in os.environ:
    plaintext = os.environ["TEXT"].lower()
if "PAD" in os.environ:
    random_pad = True if os.environ["PAD"].lower() == "y" else False


@app.route("/ciphertext_public_key", methods=["GET"])
def get_ciphertext_public_key():
    try:
        return jsonify({"ciphertext_public": ciphertexts_public_pair}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("----------Server----------")
    print("Starting server...")
    print(f"Public exponent: {e}")
    print(f"Number of receiver: {receiver}")
    print(f"Plaintext: {plaintext}")
    print(f"Random padding: {random_pad}")
    print("Genarating key pair...")
    keys = keygen.generate_keys(PRIME_BITS, e, receiver)
    ciphertexts_public_pair = keygen.encrypt_with_keys(plaintext, keys)
    print("Message encrypted")
    print("--------------------------")
    app.run(port=5000)
