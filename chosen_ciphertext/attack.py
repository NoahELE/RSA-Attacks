import time

import gmpy2
import requests

time.sleep(5)  # wait for the server to start

SERVER_URL = "http://localhost:5000"

m = 42

c = requests.post(
    f"{SERVER_URL}/encrypt",
    json={"m": m},
).json()["c"]
print(f"c: {c}")

public_key = requests.get(f"{SERVER_URL}/public_key").json()
n = public_key["n"]
e = public_key["e"]
print(f"n: {n}")
print(f"e: {e}")

r = 13
c1 = c * pow(r, e, n) % n
print(f"c1: {c1}")
m1 = requests.post(
    f"{SERVER_URL}/decrypt",
    json={"c": c1},
).json()["m"]
print(f"m1: {m1}")

m_decrypted = m1 * gmpy2.invert(r, n) % n

print(f"m_decrypted: {m_decrypted}")
