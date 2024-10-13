import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

SERVER_URL = "http://server:5000"  # to be changed to environment var


def get_public_key():
    response = requests.get(f"{SERVER_URL}/public_key")
    return RSA.import_key(response.content)


def encrypt_and_send_message(public_key, message):
    try:
        cipher = PKCS1_OAEP.new(public_key)

        # encrypt message to server, tell it to decrypt and sends it back
        ciphertext = cipher.encrypt(message.encode())
        payload = {"ciphertext": ciphertext}
        response = requests.post(f"{SERVER_URL}/decrypt", json=payload)

        return response.json()["plaintext"]
    except Exception as e:
        return f"Error occurs: {e}"


if __name__ == "__main__":
    try:
        time.sleep(5)  # hardcoded sleeper to wait for server to start
        public_key = get_public_key()
        plaintext = "Hello, server! This is a secret message."
        decrypted_message = encrypt_and_send_message(public_key, plaintext)
        print(f"Server decrypted: {decrypted_message}")
    except Exception as e:
        print(f"Error occurs: {e}")
