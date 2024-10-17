from sympy import gcd, nextprime, isprime
from random import getrandbits
import time
from typing import List


class BroadcastAttackAnalyzer:
    def __init__(
        self,
        num_receiver,
        public_exp,
        plaintext,
        num_bits=[1024],
        random_bit=None,
    ):
        self.num_receiver: List = num_receiver
        self.public_exp: List = public_exp
        self.plaintext: List = plaintext
        self.num_bits: List = num_bits
        self.random_bit = random_bit

    def init_receiver(self, num_receiver, num_bits, public_exp):
        key_pairs = []
        for _ in range(num_receiver):
            key_pairs += [
                (
                    self.generate_low_public_exponent_scheme(
                        prime_bits=num_bits, public_exp=public_exp
                    )
                )
            ]
        return key_pairs

    def check_plaintext_length(self, key_pairs, plaintext):
        for pub, _ in key_pairs:
            _, n = pub
            assert (
                plaintext < n
            ), "plaintext should be smaller than modulus to gaurantee the attack scheme"

    def encrypt_with_pub(self, key_pairs, plaintext):
        ciphertext = []
        for pub, _ in key_pairs:
            ciphertext += [self.encrypt(plaintext, pub)]
        return ciphertext

    def analyze_attack_loop(self):
        for num_rec in self.num_receiver:
            for num_bit in self.num_bits:
                for pub_exp in self.public_exp:
                    for text in self.plaintext:
                        try:
                            recovered_plaintext, time_elapsed = self.analyze_attack(
                                num_rec, pub_exp, text, num_bit
                            )
                            self.print_stat(
                                recovered_plaintext,
                                num_rec,
                                pub_exp,
                                text,
                                num_bit,
                                time_elapsed,
                            )
                        except Exception:
                            print("Cannot recover plaintext")

    def analyze_attack(self, num_receiver, public_exponent, plaintext, num_bits):
        # initialize key pairs
        key_pairs = self.init_receiver(num_receiver, num_bits, public_exponent)

        # In order for the attack to occur, we should have a relatively small plaintext
        # that is, the plaintext should be shorter than the prime
        self.check_plaintext_length(key_pairs, plaintext)

        # encrypt plaintext and "broadcast"
        ciphertext = self.encrypt_with_pub(key_pairs, plaintext)

        # Perform the low public exponent attack
        start = time.time()

        cipher, key_info = self.crt(*zip(ciphertext, [pub for pub, _ in key_pairs]))
        if key_info is not None:
            recovered_plaintext = self.decrypt_message(key_info, ciphertext)
            return recovered_plaintext, time.time() - start
        recovered_plaintext = self.cube_root(cipher)

        elapse = time.time() - start

        return recovered_plaintext, elapse

    def print_info(self, num_receiver, public_exponent, num_bits):
        print(
            f"Num receiver: { num_receiver} -- Public exp: { public_exponent} --  Num bits: {num_bits } -- Random bit: {self.random_bit }"
        )

    def print_stat(
        self,
        recovered_plaintext,
        num_receiver,
        public_exponent,
        text,
        num_bits,
        time_elapsed,
    ):
        print("\n-----STAT-----")
        print(f"Total time elapse: {time_elapsed:2f}s")
        if text == recovered_plaintext:
            print("Hacked")
        self.print_info(num_receiver, public_exponent, num_bits)
        print("--------------\n")

    def generate_prime(self, bits):
        """
        Generates the prime given the number of bits
        """
        return nextprime(getrandbits(bits))

    def generate_keypair(self, p, q, e):
        """
        Generates rsa key pair

        **p and q should have been checked for primality

        Returns the public and private key pair
        """
        n = p * q
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        return ((e, n), (d, n))

    def generate_low_public_exponent_scheme(self, prime_bits, public_exp):
        """
        Generates a vaible attack scenario for low public exponent attack
        the public exponent is set to three

        Returns the public and private key pair for the scheme
        """

        while True:
            try:
                p = self.generate_prime(prime_bits)
                q = self.generate_prime(prime_bits)
                assert isprime(p), "the generated number is not prime"
                assert isprime(q), "the generated number is not prime"
                keys = self.generate_keypair(p, q, public_exp)
                break
            except ValueError:
                continue
        return keys

    def encrypt(self, plaintext, key):
        """
        Encrypts the plaintext with the public keys

        Returns the ciphertext
        """
        e, n = key
        return pow(plaintext, e, n)

    def decrypt(self, ciphertext, key):
        """
        Dencrypts the ciphertext with the private keys

        Returns the plaintext
        """
        d, n = key
        return pow(ciphertext, d, n)

    def crt(self, *cipherpair):
        factorization, pub, idx = self.check_pairwise_coprime(cipherpair)
        if pub:
            return None, (factorization, pub, idx)

        n = 1
        for _, pub in cipherpair:
            _, n_i = pub
            n *= n_i

        re = 0
        for c, pub in cipherpair:
            _, n_i = pub
            n_c = n // n_i
            re += c * n_c * pow(n_c, -1, n_i) % n
        return re % n, None

    def cube_root(self, n):
        return round(n ** (1.0 / 3))

    def check_pairwise_coprime(self, cipherpair):
        pub_list = []
        for _, pub in cipherpair:
            pub_list += [pub]

        for i in range(len(pub_list) - 1):
            for j in range(i + 1, len(pub_list)):
                common = gcd(pub_list[i][1], pub_list[j][1])
                if common != 1:
                    return (common, pub_list[i][1] // common), pub_list[i], i
        return None, None, None

    def decrypt_message(self, key_info, ciphertext):
        factorization, pub, idx = key_info
        p, q = factorization
        e, n = pub

        phi = int((p - 1) * (q - 1))
        d = pow(e, -1, phi)
        return self.decrypt(ciphertext[idx], (d, n))


def main():
    num_receiver = [3]
    num_bits = [10]
    public_exponent = [3]
    plaintext = [102]
    attackAnalyzer = BroadcastAttackAnalyzer(
        num_receiver, public_exponent, plaintext, num_bits
    )
    attackAnalyzer.analyze_attack_loop()


if __name__ == "__main__":
    main()
