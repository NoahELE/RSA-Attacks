from sympy import gcd
from utils.keygen import decrypt
from gmpy2 import mpz
import gmpy2

gmpy2.get_context().precision = 2048


def crt(*cipherpair):
    factorization, pub, idx = check_pairwise_coprime(cipherpair)
    if pub:
        return None, (factorization, pub, idx)
    n = mpz(1)
    for _, pub in cipherpair:
        _, n_i = pub
        n *= mpz(str(n_i))

    re = 0
    for c, pub in cipherpair:
        c = mpz(c)
        _, n_i = pub
        n_i = mpz(str(n_i))
        n_c = n // n_i
        re += c * n_c * pow(n_c, -1, n_i) % n
    return re % n, None


def check_pairwise_coprime(cipherpair):
    pub_list = []
    for _, pub in cipherpair:
        pub_list += [pub]

    for i in range(len(pub_list) - 1):
        for j in range(i + 1, len(pub_list)):
            common = gcd(pub_list[i][1], pub_list[j][1])
            if common != 1:
                return (common, pub_list[i][1] // common), pub_list[i], i
    return None, None, None


def decrypt_message(key_info, ciphertext):
    factorization, pub, idx = key_info
    p, q = factorization
    e, n = pub

    phi = int((p - 1) * (q - 1))
    d = pow(e, -1, phi)
    return decrypt(ciphertext[idx], (d, n))


def convert_to_plaintext(mpz_obj):
    mpz_str = str(mpz_obj)
    string = "".join(chr(int(mpz_str[i : i + 3])) for i in range(0, len(mpz_str), 3))
    return string
