import gmpy2
import time
import random

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

def main(bits):
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

    # Save results to files in decimal, hexadecimal, and binary formats
    with open("RSA-Key.txt", "w") as file, open("hexa-RSA-Key.txt", "w") as hexFile, open("bits-RSA-Key.txt", "w") as bitsFile:
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

if __name__ == "__main__":
    bits = int(input("Enter the number of bits: "))
    if bits <= 0:
        print("Please enter a valid positive integer for the number of bits.")
    else:
        main(bits)
