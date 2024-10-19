import gmpy2
import time
import random
import os

KNOWN_BIT_PERCENTAGE = 27

def generate_distinct_primes(bit_size):
    state = gmpy2.random_state(int(time.time()))

    # Generate first prime p
    p = gmpy2.mpz_urandomb(state, bit_size)
    p = gmpy2.next_prime(p)

    # Generate distinct prime q
    q = gmpy2.mpz_urandomb(state, bit_size)
    q = gmpy2.next_prime(q)
    
    while q == p:
        q = gmpy2.mpz_urandomb(state, bit_size)
        q = gmpy2.next_prime(q)
    
    return p, q

def save_to_bit_file(file, num):
    # Convert num to binary string and write to file
    bit_str = num.digits(2)
    file.write(f"{bit_str}\n")

def generate_bin_hex_dec_key_files(key_directory, bits):
    p, q = generate_distinct_primes(bits)
    
    # Compute n = p * q
    n = p * q

    # e is typically 65537
    e = gmpy2.mpz(65537)

    # Compute phi(n) = (p-1)(q-1)
    p_1 = p - 1
    q_1 = q - 1
    phi = p_1 * q_1

    # Compute d = e^-1 mod phi
    try:
        d = gmpy2.invert(e, phi)
    except ZeroDivisionError:
        raise ValueError("Failed to compute d. e and phi are not coprime.")

    # Compute dp = d mod (p-1) and dq = d mod (q-1)
    dp = d % p_1
    dq = d % q_1

    # Compute qp = q^-1 mod p
    try:
        qp = gmpy2.invert(q, p)
    except ZeroDivisionError:
        raise ValueError("Failed to compute inverse of q mod p.")
    
    if not os.path.exists(key_directory):
        os.makedirs(key_directory)

    keys_paths = {}
    keys_paths['dec'] = key_directory + "RSA-Key.txt"
    keys_paths['hex'] = key_directory + "hexa-RSA-Key.txt"
    keys_paths['bin'] = key_directory + "bits-RSA-Key.txt"
    
    keys_public_directory = key_directory.rstrip('/') + '_public/'
    if not os.path.exists(keys_public_directory):
        os.makedirs(keys_public_directory)

    keys_public_paths = {}
    keys_public_paths['dec'] = keys_public_directory + "RSA-Key.txt"
    keys_public_paths['hex'] = keys_public_directory + "hexa-RSA-Key.txt"
    keys_public_paths['bin'] = keys_public_directory + "bits-RSA-Key.txt"

    # Save results to files in decimal, hexadecimal, and binary formats
    with open(keys_paths['dec'], "w") as file, open(keys_paths['hex'], "w") as hexFile, open(keys_paths['bin'], "w") as bitsFile:
        # Save in decimal format
        file.write(f"N={n.digits(10)}\n")
        file.write(f"e={e.digits(10)}\n")
        file.write(f"d={d.digits(10)}\n")
        file.write(f"p={p.digits(10)}\n")
        file.write(f"q={q.digits(10)}\n")
        file.write(f"dp={dp.digits(10)}\n")
        file.write(f"dq={dq.digits(10)}\n")
        file.write(f"qp={qp.digits(10)}\n")

        # Save in hexadecimal format
        hexFile.write(f"N={n.digits(16)}\n")
        hexFile.write(f"e={e.digits(16)}\n")
        hexFile.write(f"d={d.digits(16)}\n")
        hexFile.write(f"p={p.digits(16)}\n")
        hexFile.write(f"q={q.digits(16)}\n")
        hexFile.write(f"dp={dp.digits(16)}\n")
        hexFile.write(f"dq={dq.digits(16)}\n")
        hexFile.write(f"qp={qp.digits(16)}\n")

        # Save in binary format
        bitsFile.write("N=")
        save_to_bit_file(bitsFile, n)
        bitsFile.write("e=")
        save_to_bit_file(bitsFile, e)
        bitsFile.write("d=")
        save_to_bit_file(bitsFile, d)
        bitsFile.write("p=")
        save_to_bit_file(bitsFile, p)
        bitsFile.write("q=")
        save_to_bit_file(bitsFile, q)
        bitsFile.write("dp=")
        save_to_bit_file(bitsFile, dp)
        bitsFile.write("dq=")
        save_to_bit_file(bitsFile, dq)
        bitsFile.write("qp=")
        save_to_bit_file(bitsFile, qp)

    # Save results to files in decimal, hexadecimal, and binary formats
    with open(keys_public_paths['dec'], "w") as file, open(keys_public_paths['hex'], "w") as hexFile, open(keys_public_paths['bin'], "w") as bitsFile:
        # Save in decimal format
        file.write(f"N={n.digits(10)}\n")
        file.write(f"e={e.digits(10)}\n")

        # Save in hexadecimal format
        hexFile.write(f"N={n.digits(16)}\n")
        hexFile.write(f"e={e.digits(16)}\n")

        # Save in binary format
        bitsFile.write("N=")
        save_to_bit_file(bitsFile, n)
        bitsFile.write("e=")
        save_to_bit_file(bitsFile, e)

    return keys_paths

class KnownBit:
    def __init__(self, position, value):
        self.position = position
        self.value = value

def read_and_convert_component(component, file):
    for line in file:
        if '=' in line:
            hex_str = line.split('=')[1].strip()  # skip '='
            component = gmpy2.mpz(hex_str, 16)
            return component

def degrade_component(component, filename):
    total_bits = component.bit_length()
    known_bit_count = (total_bits * KNOWN_BIT_PERCENTAGE) // 100
    all_bits = [KnownBit(i, -1) for i in range(total_bits)]  # init to -1

    # create a list of indices of all bits and shuffle them randomly
    indices = list(range(total_bits))
    random.seed(time.time())
    random.shuffle(indices)

    # the first known_bit_count known bits
    for i in range(known_bit_count):
        bit_value = gmpy2.bit_test(component, indices[i])
        all_bits[indices[i]].value = int(bit_value)

    with open(filename, "w") as file:
        for bit in all_bits:
            file.write(f"{bit.position} {bit.value}\n")

def generate_known_bits_as_cold_start_attack(key_directory, known_bits_directory):
    rsa_components = ["n", "e", "d", "p", "q", "dp", "dq", "qp"]
    rsa_values = {}

    # get key values from hexa-RSA-Key.txt and convert component
    with open(key_directory + "hexa-RSA-Key.txt", "r") as rsakey_file:
        for component in rsa_components:
            rsa_values[component] = gmpy2.mpz(0)
            rsa_values[component] = read_and_convert_component(rsa_values[component], rsakey_file)

    if not os.path.exists(known_bits_directory):
        os.makedirs(known_bits_directory)

    known_bits_paths = {}
    known_bits_paths['n'] = known_bits_directory + "known_bits_n.txt"
    known_bits_paths['e'] = known_bits_directory + "known_bits_e.txt"
    known_bits_paths['d'] = known_bits_directory + "known_bits_d.txt"
    known_bits_paths['p'] = known_bits_directory + "known_bits_p.txt"
    known_bits_paths['q'] = known_bits_directory + "known_bits_q.txt"
    known_bits_paths['dp'] = known_bits_directory + "known_bits_dp.txt"
    known_bits_paths['dq'] = known_bits_directory + "known_bits_dq.txt"
    known_bits_paths['qp'] = known_bits_directory + "known_bits_qp.txt"


    # seperately 
    degrade_component(rsa_values["n"], known_bits_paths['n'])
    degrade_component(rsa_values["e"], known_bits_paths['e'])
    degrade_component(rsa_values["d"], known_bits_paths['d'])
    degrade_component(rsa_values["p"], known_bits_paths['p'])
    degrade_component(rsa_values["q"], known_bits_paths['q'])
    degrade_component(rsa_values["dp"], known_bits_paths['dp'])
    degrade_component(rsa_values["dq"], known_bits_paths['dq'])
    degrade_component(rsa_values["qp"], known_bits_paths['qp'])

    return known_bits_paths

if __name__ == "__main__":
    bits = int(input("Enter the number of bits(for p and q): "))
    if bits <= 0:
        print("Please enter a valid positive integer for the number of bits.")
    else:
        # do not give this to attacker
        key_directory = './keys/'
        keys_paths = generate_bin_hex_dec_key_files(key_directory, bits)

        # attacker can get these files simulate the cold start attack, the num of bits known is set in KNOWN_BIT_PERCENTAGE
        known_bits_directory = './known_bits_files/'
        known_bits_paths = generate_known_bits_as_cold_start_attack(key_directory, known_bits_directory)


