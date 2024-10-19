import gmpy2
import numpy as np
import sys

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

def guess_bits_and_compute_degraded_d(mod_filename):
    binary_number = None
    try:
        with open(mod_filename, "r") as mod_file:
            binary_number = gmpy2.mpz(0)
            for line in mod_file:
                position, value = map(int, line.split())

                # set all -1 as 1
                if value == -1:
                    value = 1

                # Place it on the corresponding position using gmpy2 mpz operations
                binary_number |= (gmpy2.mpz(value) << position)

        # print degraded_d
        print(f"Final value of d (as gmpy2.mpz): {binary_number}")

    except FileNotFoundError as e:
        print(f"Failed to open file: {e}")
    except ValueError as e:
        print(f"Data Processed Error: {e}")

    return binary_number

def get_N_e_from_public_key_file(key_public_filename):
    N = None
    e = None
    find_N = False
    find_e = False
    
    try:
        with open(key_public_filename, "r") as file:
            for line in file:
                line = line.strip() 
                
                if line.startswith("N="):
                    N = gmpy2.mpz(line.split('=')[1].strip())
                    find_N = True
                elif line.startswith("e="):
                    e = gmpy2.mpz(line.split('=')[1].strip())
                    find_e = True
    except FileNotFoundError:
        print(f"File {key_public_filename} not found.")
    except ValueError:
        print(f"Error in file format. Ensure the values for N and e are valid integers. Find N = {find_N}, Find e = {find_e}")

    return N, e

def get_known_bits_file_names(known_bits_directory, keys_public_directory):
    known_bits_paths = {}
    known_bits_paths['n'] = known_bits_directory + "known_bits_n.txt"
    known_bits_paths['e'] = known_bits_directory + "known_bits_e.txt"
    known_bits_paths['d'] = known_bits_directory + "known_bits_d.txt"
    known_bits_paths['p'] = known_bits_directory + "known_bits_p.txt"
    known_bits_paths['q'] = known_bits_directory + "known_bits_q.txt"
    known_bits_paths['dp'] = known_bits_directory + "known_bits_dp.txt"
    known_bits_paths['dq'] = known_bits_directory + "known_bits_dq.txt"
    known_bits_paths['qp'] = known_bits_directory + "known_bits_qp.txt"

    keys_public_paths = {}
    keys_public_paths['dec'] = keys_public_directory + "RSA-Key.txt"
    keys_public_paths['hex'] = keys_public_directory + "hexa-RSA-Key.txt"
    keys_public_paths['bin'] = keys_public_directory + "bits-RSA-Key.txt"

    return known_bits_paths, keys_public_paths

def calculate_k_kp_kq_from_N_e_degraded_d(known_bits_d_path, dec_key_public_path):
    degraded_d = guess_bits_and_compute_degraded_d(known_bits_d_path)
    N, e = get_N_e_from_public_key_file(dec_key_public_path)

    if N is None or e is None or degraded_d is None:
        print(f"Find degraded_d, N, e Error, please check file and path. degraded_d: {degraded_d}, N: {N}, e: {e}")

        return None

    print("Find degraded_d, N, e Successfully, Now calculating kp and kq, hold still...")

    k, d_of_k = calculate_k(N, e, degraded_d)

    d_corrected_msb = correct_msb_half_d(d_of_k, degraded_d)
    print(f"d_corrected_msb={d_corrected_msb}")

    print(f"k={k}")

    kp, kq = solve_quad(N, e, k)

    print(f"kp={kp} kq={kq}")

    return k, kp, kq, N, e

# Part 2

# Define the ValidSolution class
class ValidSolution:
    def __init__(self):
        self.slice = ['0'] * 5

# Read files that store known bits
def read_known_bits(filename):
    known_bits = np.full(4096, -1)  # Initialize with -1
    try:
        with open(filename, 'r') as file:
            for line in file:
                index, value = map(int, line.split())
                if index < 4096:
                    known_bits[index] = value
    except IOError:
        print(f"Error opening file: {filename}")
    return known_bits

def read_component(file):
    buffer = file.readline().strip()
    return gmpy2.mpz(buffer.split('=')[1].strip())

# Utility function to get the ith bit of a GMP number
def get_gmp_bit(number, i):
    return int(gmpy2.bit_test(number, i))

# Equation 8
def equation_8(N, p0, q0, p_i, q_i, i):
    term = (p0 * q0)
    term = N - term
    return get_gmp_bit(term, i) == (p_i ^ q_i)

# Equation 9
def equation_9(N, e, k, tau_k, p0, q0, d0, p_i, q_i, d_tau_k_i, i):
    term = k * (N + 1)
    temp = p0 + q0
    term -= k * temp
    term -= e * d0
    term += 1
    return get_gmp_bit(term, i + tau_k) == (d_tau_k_i ^ p_i ^ q_i)

# Equation 10
def equation_10(e, kp, tau_kp, p0, dp0, p_i, dp_i, i):
    term = kp * (p0 - 1) + 1 - (e * dp0)
    return get_gmp_bit(term, i + tau_kp) == (dp_i ^ p_i)

# Equation 11
def equation_11(e, kq, tau_kq, q0, dq0, q_i, dq_i, i):
    term = kq * (q0 - 1) + 1 - (e * dq0)
    return get_gmp_bit(term, i + tau_kq) == (dq_i ^ q_i)

# Compute τ(x), the exponent of the largest power of 2 dividing x
def tau(x):
    count = 0
    while x % 2 == 0:
        x //= 2
        count += 1
    return count

# Function to correct the least significant bits for dp, dq, d
def correct_lsb(e, k, tau_k, is_d):
    power = 2 + tau_k if is_d else 1 + tau_k
    modulus = gmpy2.mpz(2) ** power
    return gmpy2.invert(e, modulus)

# Core function for the first phase of the RSA key reconstruction algorithm
def reconstruct_rsa_key_first_phase(p, q, d, dp, dq, e, k, kp, kq):
    p = p.bit_set(0)  # p is odd
    q = q.bit_set(0)  # q is odd

    tau_kp = tau(kp)
    tau_kq = tau(kq)
    tau_k = tau(k)

    dp = correct_lsb(e, kp, tau_kp, False)
    dq = correct_lsb(e, kq, tau_kq, False)
    d = correct_lsb(e, k, tau_k, True)

    return p, q, dp, dq, d

# Calculating p and q from my_dp and my_dq
def compute_qp_from_dpq(e, k, temp_dp):
    result = (e * temp_dp - 1) // k + 1
    # result = gmpy2.divexact(result, k)
    # result += 1
    print("result: ", result)
    return result

def calculate_d(p, q, e):
    phi = (p - 1) * (q - 1)
    return gmpy2.invert(e, phi)

# The core of the Heninger-Shacham algorithm
def branch_and_prune(result_p, result_q, my_p, my_q, my_d, my_dp, my_dq, 
                     e, k, kp, kq, N, tau_k, tau_kp, tau_kq,
                     possibilities, num_possibilities, known_bits_p,
                     known_bits_q, known_bits_d, known_bits_dp,
                     known_bits_dq, verbose, counter):
    valid_solutions = []
    valid_solutions_count = 0 
    result_n = gmpy2.mpz(0)
    result_d = gmpy2.mpz(0)
    final_solution = {}
    final_solution['fail'] = -1

    for i in range(num_possibilities):
        possibility = possibilities[i]
        print(possibility)
        print(equation_8(N, my_p, my_q, possibility[0], possibility[1], counter), 
            equation_9(N, e, k, tau_k, my_p, my_q, my_d, possibility[0], possibility[1], possibility[2], counter), 
            equation_10(e, kp, tau_kp, my_p, my_dp, possibility[0], possibility[3], counter), 
            equation_11(e, kq, tau_kq, my_q, my_dq, possibility[1], possibility[4], counter))
        if (equation_8(N, my_p, my_q, possibility[0], possibility[1], counter) and
            equation_9(N, e, k, tau_k, my_p, my_q, my_d, possibility[0], possibility[1], possibility[2], counter) and
            equation_10(e, kp, tau_kp, my_p, my_dp, possibility[0], possibility[3], counter) and
            equation_11(e, kq, tau_kq, my_q, my_dq, possibility[1], possibility[4], counter)):
            
            matches_known_bits = True
            print("bool inside: ", (known_bits_p[counter] != -1 and known_bits_p[counter] != int(possibility[0])),
                (known_bits_q[counter] != -1 and known_bits_q[counter] != int(possibility[1])),
                (known_bits_d[counter + tau_k] != -1 and known_bits_d[counter + tau_k] != int(possibility[2])),
                (known_bits_dp[counter + tau_kp] != -1 and known_bits_dp[counter + tau_kp] != int(possibility[3])),
                (known_bits_dq[counter + tau_kq] != -1 and known_bits_dq[counter + tau_kq] != int(possibility[4])))
            if ((known_bits_p[counter] != -1 and known_bits_p[counter] != int(possibility[0])) or
                (known_bits_q[counter] != -1 and known_bits_q[counter] != int(possibility[1])) or
                (known_bits_d[counter + tau_k] != -1 and known_bits_d[counter + tau_k] != int(possibility[2])) or
                (known_bits_dp[counter + tau_kp] != -1 and known_bits_dp[counter + tau_kp] != int(possibility[3])) or
                (known_bits_dq[counter + tau_kq] != -1 and known_bits_dq[counter + tau_kq] != int(possibility[4]))):
                matches_known_bits = False
                # print(f"counter: {counter}")
                # print(f"possibility: ", possibility)

            if matches_known_bits:
                valid_solution = ValidSolution()

                for j in range(5):
                    valid_solution.slice[j] = possibility[j]
                valid_solution.slice = possibility
                valid_solutions.append(valid_solution)
                valid_solutions_count += 1
                print("slice before valid: ", valid_solutions[valid_solutions_count-1].slice)
                
                if verbose:
                    print(f"Valid combination for Slice({counter}): "
                          f"p[{counter}]={possibility[0]}, q[{counter}]={possibility[1]}, "
                          f"d[{tau_k + counter}]={possibility[2]}, "
                          f"dp[{tau_kp + counter}]={possibility[3]}, "
                          f"dq[{tau_kq + counter}]={possibility[4]}")
                    print(f"------------------------------------------------------------\nThe value of my p is : {my_p}")
                    print(f"The value of my q is : {my_q}")
                    print(f"The value of my d is : {my_d}")
                    print(f"The value of my dp is : {my_dp}")
                    print(f"The value of my dq is : {my_dq}\n------------------------------------------------------------")

                print("e, kp, my_dp: ", e, kp, my_dp)
                print("e, kq, my_dq: ", e, kq, my_dq)
                result_p = compute_qp_from_dpq(e, kp, my_dp)
                result_q = compute_qp_from_dpq(e, kq, my_dq)
                result_n = result_p * result_q
                print("result_p, result_q: ", result_p, result_q)
                print(f"The value of result_n is : {result_n}, N: {N}")
                
                if result_n == N:
                    print("find solution")
                    result_d = calculate_d(result_p, result_q, e)
                    final_solution['p'] = result_p
                    final_solution['q'] = result_q
                    final_solution['d'] = result_d
                    final_solution['dp'] = my_dp
                    final_solution['dq'] = my_dq
                    final_solution['fail'] = 0

                    return result_p, result_q, final_solution
                elif result_n > N * 10:
                    final_solution['fail'] = 1
                    return result_p, result_q, final_solution
                

    for valid_solution in valid_solutions:
        cloned_my_p = my_p
        cloned_my_q = my_q
        cloned_my_d = my_d
        cloned_my_dp = my_dp
        cloned_my_dq = my_dq
        print("ATTENTAION_PRE: ", cloned_my_p, cloned_my_q, cloned_my_d,
                         cloned_my_dp, cloned_my_dq)

        slice = valid_solution.slice
        print("slice: ", slice, "counter: ", counter, tau_k, tau_kp, tau_kq)
        if slice[0] == 1:
            cloned_my_p = cloned_my_p.bit_set(counter)
        if slice[1] == 1:
            cloned_my_q = cloned_my_q.bit_set(counter)
        if slice[2] == 1:
            cloned_my_d = cloned_my_d.bit_set(counter + tau_k)
        if slice[3] == 1:
            cloned_my_dp = cloned_my_dp.bit_set(counter + tau_kp)
        if slice[4] == 1:
            cloned_my_dq = cloned_my_dq.bit_set(counter + tau_kq)
        print("ATTENTAION: ", cloned_my_p, cloned_my_q, cloned_my_d,
                         cloned_my_dp, cloned_my_dq)
        result_p, result_q, final_solution = branch_and_prune(result_p, result_q, cloned_my_p, cloned_my_q, cloned_my_d,
                         cloned_my_dp, cloned_my_dq, e, k, kp, kq, N, tau_k, tau_kp,
                         tau_kq, possibilities, num_possibilities, known_bits_p,
                         known_bits_q, known_bits_d, known_bits_dp, known_bits_dq,
                         verbose, counter + 1)
        if final_solution['fail'] != -1:
            break
    return result_p, result_q, final_solution


def recovered_d_by_recursion(k, kp, kq, N, e, known_bits_paths):
    system_recursion_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(10**6)
    print(f"Temp set recursion limit from {system_recursion_limit} to 10**6")
    verbose = True 
    counter = 1

    possibilities = [
        (0, 0, 0, 0, 0), (0, 0, 0, 0, 1), (0, 0, 0, 1, 0), (0, 0, 0, 1, 1),
        (0, 0, 1, 0, 0), (0, 0, 1, 0, 1), (0, 0, 1, 1, 0), (0, 0, 1, 1, 1),
        (0, 1, 0, 0, 0), (0, 1, 0, 0, 1), (0, 1, 0, 1, 0), (0, 1, 0, 1, 1),
        (0, 1, 1, 0, 0), (0, 1, 1, 0, 1), (0, 1, 1, 1, 0), (0, 1, 1, 1, 1),
        (1, 0, 0, 0, 0), (1, 0, 0, 0, 1), (1, 0, 0, 1, 0), (1, 0, 0, 1, 1),
        (1, 0, 1, 0, 0), (1, 0, 1, 0, 1), (1, 0, 1, 1, 0), (1, 0, 1, 1, 1),
        (1, 1, 0, 0, 0), (1, 1, 0, 0, 1), (1, 1, 0, 1, 0), (1, 1, 0, 1, 1),
        (1, 1, 1, 0, 0), (1, 1, 1, 0, 1), (1, 1, 1, 1, 0), (1, 1, 1, 1, 1)
    ]  # Initialize possibilities for each slice

    my_p = gmpy2.mpz(0)
    my_q = gmpy2.mpz(0)
    my_d = gmpy2.mpz(0)
    my_dp = gmpy2.mpz(0)
    my_dq = gmpy2.mpz(0)
    result_p = gmpy2.mpz(0)
    result_q = gmpy2.mpz(0)

    # init
    my_p = gmpy2.mpz(0)
    my_q = gmpy2.mpz(0)
    my_d = gmpy2.mpz(0)
    my_dp = gmpy2.mpz(0)
    my_dq = gmpy2.mpz(0)

    known_bits_p = [0] * 4096
    known_bits_q = [0] * 4096
    known_bits_d = [0] * 9192
    known_bits_dp = [0] * 4096
    known_bits_dq = [0] * 4096

    known_bits_p = read_known_bits(known_bits_paths['p'])
    known_bits_q = read_known_bits(known_bits_paths['q'])
    known_bits_d = read_known_bits(known_bits_paths['d'])
    known_bits_dp = read_known_bits(known_bits_paths['dp'])
    known_bits_dq = read_known_bits(known_bits_paths['dq'])

    # First phase of RSA key reconstruction
    my_p, my_q, my_dp, my_dq, my_d = reconstruct_rsa_key_first_phase(my_p, my_q, my_d, my_dp, my_dq, e, k, kp, kq)

    # Calculate τ values ​​for k, kp, and kq
    tau_k = tau(k)
    tau_kp = tau(kp)
    tau_kq = tau(kq)

    # 打印初始位
    print(f"Correction: p[0]={my_p}, q[0]={my_q}, d[{tau_k + 2}]={my_d}, "
        f"dp[{tau_kp + 1}]={my_dp}, dq[{tau_kq + 1}]={my_dq}")

    print(f"Slice(0): p[0]={get_gmp_bit(my_p, 0)}, q[0]={get_gmp_bit(my_q, 0)}, "
        f"d[{tau_k}]={get_gmp_bit(my_d, tau_k)}, dp[{tau_kp}]={get_gmp_bit(my_dp, tau_kp)}, "
        f"dq[{tau_kq}]={get_gmp_bit(my_dq, tau_kq)}")
    
    # Start Recursion!
    result_p, result_q, final_solution = branch_and_prune(result_p, result_q, my_p, my_q, my_d, my_dp, my_dq, e, k, kp, kq, N, tau_k, tau_kp, tau_kq, 
                    possibilities, 32, known_bits_p, known_bits_q, known_bits_d, known_bits_dp, known_bits_dq, verbose, 1)
    print(f"FIRST Recursion END, result_p: {result_p}, result_q: {result_q}")

    if final_solution['fail'] != 0:
        print(f"Not solve, Swap kp and kq and restart recursion")
        result_p, result_q, final_solution = branch_and_prune(result_p, result_q, my_p, my_q, my_d, my_dp, my_dq, e, k, kq, kp, N, tau_k, tau_kq, tau_kp, 
                        possibilities, 32, known_bits_p, known_bits_q, known_bits_d, known_bits_dp, known_bits_dq, verbose, 1)

    sys.setrecursionlimit(system_recursion_limit)
    print(f"Function end, set recursion limit back to {system_recursion_limit}.")

    return final_solution

if __name__ == "__main__":
    known_bits_directory = './known_bits_files/'
    keys_public_directory = './keys_public/'
    known_bits_paths, keys_public_paths = get_known_bits_file_names(known_bits_directory, keys_public_directory)
    k, kp, kq, N, e = calculate_k_kp_kq_from_N_e_degraded_d(known_bits_paths['d'], keys_public_paths['dec'])
    print(k, kp, kq, N, e)

    final_solution = recovered_d_by_recursion(k, kp, kq, N, e, known_bits_paths)
    
    if final_solution['fail'] != 0:
        print(f"Solve problem failed, please increase KNOWN_BIT_PERCENTAGE.")
    else:
        print(f"Problem solved!!!!")
        print("\n------------------------------------------------------------\n\t\t\tResults:\n------------------------------------------------------------\n")
        print(f"The correct value of p is : {final_solution['p']}")
        print(f"The correct value of q is : {final_solution['q']}")
        print(f"The correct value of d is : {final_solution['d']}")
        print(f"The correct value of dp is : {final_solution['dp']}")
        print(f"The correct value of dq is : {final_solution['dq']}")