import gmpy2

def calculate_k(N, e, degraded_d):
    max_matching_bits = 0
    matching_bits = 0
    k = gmpy2.mpz(1)
    d_tilde = gmpy2.mpz(0)
    temp = gmpy2.mpz(0)
    N_plus_1 = N + 1
    new_d_tilde = gmpy2.mpz(0)
    new_k = gmpy2.mpz(0)

    total_bits = degraded_d.bit_length()
    bits_to_compare = (total_bits // 2) - 2  # Compare down to (n/2) - 2

    # Loop to find possible values of k between 1 and e-1 and calculate d_tilde
    while k < e:
        # d_tilde(k) = (k(N + 1) + 1) / e
        temp = k * N_plus_1 + 1
        d_tilde = temp // e

        matching_bits = 0
        for i in range(bits_to_compare):
            bit_index = total_bits - i - 1  # Calculate the index of the bit to compare
            if gmpy2.bit_test(d_tilde, bit_index) == gmpy2.bit_test(degraded_d, bit_index):
                matching_bits += 1  # Increment match count if the bits are the same

        if matching_bits > max_matching_bits:
            max_matching_bits = matching_bits
            new_k = k
            new_d_tilde = d_tilde

        k += 1  # Increment k

    print(f"Matching d_tilde for k={new_k}: {new_d_tilde}")
    return new_k, new_d_tilde


def correct_msb_half_d(A, B):
    # Calculate the total number of bits in A
    total_bits = A.bit_length()

    # Calculate the number of bits to take from A (MSBs)
    msb_bits = (total_bits // 2) - 2

    # Create a bitmask for the MSB part of A
    mask = (1 << msb_bits) - 1
    mask <<= (total_bits - msb_bits)

    # Isolate MSBs from A
    C = A & mask

    # Create a bitmask for the LSB part of B
    mask = (1 << (total_bits - msb_bits)) - 1

    # Isolate LSBs from B
    temp = B & mask

    # Combine LSBs from B into C
    C |= temp

    return C


def tonelli_shanks(n, p):
    Q = p - 1
    S = 0
    while gmpy2.is_even(Q):
        Q //= 2
        S += 1

    z = gmpy2.mpz(2)
    while gmpy2.legendre(z, p) != -1:
        z += 1

    c = gmpy2.powmod(z, Q, p)
    t = gmpy2.powmod(n, Q, p)
    R = gmpy2.powmod(n, (Q + 1) // 2, p)

    while t != 0 and t != 1:
        M = 0
        temp = t

        while temp != 1:
            temp = gmpy2.powmod(temp, 2, p)
            M += 1

        if M == S:
            return None  # No solution

        exponent = S - M - 1
        b = gmpy2.powmod(2, exponent, p)
        b = gmpy2.powmod(c, b, p)

        c = gmpy2.powmod(b, 2, p)
        t = (t * c) % p
        R = (R * b) % p
        S = M

    if t == 1:
        return R, -R % p
    else:
        return None


def solve_quad(N, e, k):
    A = N - 1
    A = (A * k + 1 + e) // 2 % e  # First term
    B = (A * A + k) % e

    solutions = tonelli_shanks(B, e)
    if solutions is None:
        return None, None

    potential_kp = (solutions[0] + A) % e
    potential_kq = (solutions[1] + A) % e

    return potential_kp, potential_kq


def main():
    N = gmpy2.mpz("34549061992822194648111259413668094251042717858398898251961438301463949170648993062558649235309630698823673231014850314981152965831529609200399181403381235025479756924766400397718974735767937432128066946715291477973569410886645719898963698778390396489764380868721050176093749381648817527209925003315770410201")
    e = gmpy2.mpz("65537")
    d_degraded = gmpy2.mpz("88206588595944375582665472934663462930692196785338089812005584151831270494095937605618837509753609475177846142514984635760820105849909432435912788437329095997910282704927025186437525595001868241874346930847169536097230685037969758910612299331415112960574983098040417174756718456000138997417877393065000984")

    k, d_of_k = calculate_k(N, e, d_degraded)

    print(f"k={k}")

    d_corrected_msb = correct_msb_half_d(d_of_k, d_degraded)

    print(f"d_corrected_msb={d_corrected_msb}")

    print("Now calculating kp and kq, hold still...")
    
    kp, kq = solve_quad(N, e, k)

    print(f"kp={kp} kq={kq}")


if __name__ == "__main__":
    main()
