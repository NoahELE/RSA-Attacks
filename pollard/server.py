import gmpy2
from flask import Flask, jsonify, request

app = Flask(__name__)

p = int(gmpy2.next_prime(2**8))
q = int(gmpy2.next_prime(2**9))
n = p * q
e = 65537
d = int(gmpy2.invert(e, (p - 1) * (q - 1)))
print(f"p: {p} q: {q} n: {n} e: {e} d: {d}")


@app.route("/public_key", methods=["GET"])
def get_public_key():
    return jsonify({"n": n, "e": e})


@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.json
    m = data["m"]
    return jsonify({"c": m**e % n})


@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = request.json
    c = data["c"]
    return jsonify({"m": c**d % n})


if __name__ == "__main__":
    app.run(port=5000)
