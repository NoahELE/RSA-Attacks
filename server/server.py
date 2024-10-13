from flask import Flask, request, jsonify
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

app = Flask(__name__)


key = RSA.generate(1024)
pub_key = key.publickey().export_key()  # export the key to be marshalled
priv_key = key.export_key()


@app.route("/public_key", methods=["GET"])
def get_public_key():
    return pub_key


@app.route("/decrypt", methods=["POST"])
def decrypt_message_and_reply():
    try:
        data = request.json
        if not data:
            raise ValueError("Invalid json format")
        ciphertext = data["ciphertext"]
        cipher = PKCS1_OAEP.new(RSA.import_key(priv_key))
        plaintext = cipher.decrypt(ciphertext)
        return jsonify({"plaintext": plaintext}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="localhost", port=5050)
