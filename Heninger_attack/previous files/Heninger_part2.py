import gmpy2
import numpy as np

# Define the ValidSolution class
class ValidSolution:
    def __init__(self):
        self.slice = ['0'] * 5

# Read files that store known bits
def read_known_bits(filename):
    known_bits = np.full(2048, -1)  # Initialize with -1
    try:
        with open(filename, 'r') as file:
            for line in file:
                index, value = map(int, line.split())
                if index < 2048:
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
    is_solved = False

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
                    is_solved = True
                    print("\n------------------------------------------------------------\n\t\t\tResults:\n------------------------------------------------------------\n")
                    print(f"The correct value of p is : {result_p}")
                    print(f"The correct value of q is : {result_q}")
                    result_d = calculate_d(result_p, result_q, e)
                    print(f"The correct value of d is : {result_d}")
                    print(f"The correct value of dp is : {my_dp}")
                    print(f"The correct value of dq is : {my_dq}")
                    return result_p, result_q, is_solved

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
        result_p, result_q, is_solved = branch_and_prune(result_p, result_q, cloned_my_p, cloned_my_q, cloned_my_d,
                         cloned_my_dp, cloned_my_dq, e, k, kp, kq, N, tau_k, tau_kp,
                         tau_kq, possibilities, num_possibilities, known_bits_p,
                         known_bits_q, known_bits_d, known_bits_dp, known_bits_dq,
                         verbose, counter + 1)
        if is_solved:
            break
    return result_p, result_q, is_solved
import sys
def main():
    print(sys.getrecursionlimit())  # 查看当前递归深度限制
    sys.setrecursionlimit(10**6)     # 将递归深度限制调整到 2000
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

    # 初始化大整数
    e = gmpy2.mpz(0)
    k = gmpy2.mpz(0)
    kp = gmpy2.mpz(0)
    kq = gmpy2.mpz(0)
    N = gmpy2.mpz(0)
    p = gmpy2.mpz(0)
    q = gmpy2.mpz(0)
    d = gmpy2.mpz(0)
    dp = gmpy2.mpz(0)
    dq = gmpy2.mpz(0)
    my_p = gmpy2.mpz(0)
    my_q = gmpy2.mpz(0)
    my_d = gmpy2.mpz(0)
    my_dp = gmpy2.mpz(0)
    my_dq = gmpy2.mpz(0)
    result_p = gmpy2.mpz(0)
    result_q = gmpy2.mpz(0)

    # 设置初始值
    my_p = gmpy2.mpz(0)  # 等价于 mpz_set_ui(my_p, 0);
    my_q = gmpy2.mpz(0)  # 等价于 mpz_set_ui(my_q, 0);
    my_d = gmpy2.mpz(0)  # 等价于 mpz_set_ui(my_d, 0);
    my_dp = gmpy2.mpz(0)  # 等价于 mpz_set_ui(my_dp, 0);
    my_dq = gmpy2.mpz(0)  # 等价于 mpz_set_ui(my_dq, 0);

    # 设置 k, kp, kq 的值
    k = gmpy2.mpz(21643)
    kp = gmpy2.mpz(42011)
    kq = gmpy2.mpz(1976)

    # Set value for N (example value, replace with actual value)
    with open("RSA-Key.txt", "r") as file:
        N = read_component(file)

    # Set the value for e (common RSA public exponent)
    e = gmpy2.mpz(65537)

    known_bits_p = [0] * 2048
    known_bits_q = [0] * 2048
    known_bits_d = [0] * 4096
    known_bits_dp = [0] * 2048
    known_bits_dq = [0] * 2048

    known_bits_p = read_known_bits("known_bits_p.txt")
    known_bits_q = read_known_bits("known_bits_q.txt")
    known_bits_d = read_known_bits("known_bits_d.txt")
    known_bits_dp = read_known_bits("known_bits_dp.txt")
    known_bits_dq = read_known_bits("known_bits_dq.txt")

    # 第一阶段的 RSA 密钥重构
    my_p, my_q, my_dp, my_dq, my_d = reconstruct_rsa_key_first_phase(my_p, my_q, my_d, my_dp, my_dq, e, k, kp, kq)

    # 计算 k、kp 和 kq 的 τ 值
    tau_k = tau(k)
    tau_kp = tau(kp)
    tau_kq = tau(kq)

    # 打印初始位
    print(f"Correction: p[0]={my_p}, q[0]={my_q}, d[{tau_k + 2}]={my_d}, "
        f"dp[{tau_kp + 1}]={my_dp}, dq[{tau_kq + 1}]={my_dq}")

    print(f"Slice(0): p[0]={get_gmp_bit(my_p, 0)}, q[0]={get_gmp_bit(my_q, 0)}, "
        f"d[{tau_k}]={get_gmp_bit(my_d, tau_k)}, dp[{tau_kp}]={get_gmp_bit(my_dp, tau_kp)}, "
        f"dq[{tau_kq}]={get_gmp_bit(my_dq, tau_kq)}")
    
    # print(result_p, result_q, my_p, my_q, my_d, my_dp, my_dq, e, k, kp, kq, N, tau_k, tau_kp, tau_kq, 
    #                 possibilities, 32, known_bits_p, known_bits_q, known_bits_d, known_bits_dp, known_bits_dq, verbose, counter)

    # 开始 Heninger 和 Shacham 的核心算法
    result_p, result_q, is_solved = branch_and_prune(result_p, result_q, my_p, my_q, my_d, my_dp, my_dq, e, k, kp, kq, N, tau_k, tau_kp, tau_kq, 
                    possibilities, 32, known_bits_p, known_bits_q, known_bits_d, known_bits_dp, known_bits_dq, verbose, 1)
    print("FIRST END, ", result_p, result_q)

    if not is_solved:
    # 切换 Kp 和 Kq 进行第二次执行
        result_p, result_q, is_solved = branch_and_prune(result_p, result_q, my_p, my_q, my_d, my_dp, my_dq, e, k, kq, kp, N, tau_k, tau_kq, tau_kp, 
                        possibilities, 32, known_bits_p, known_bits_q, known_bits_d, known_bits_dp, known_bits_dq, verbose, 1)
    # print(result_p, result_q, my_p, my_q, my_d, my_dp, my_dq, e, k, kp, kq, N, tau_k, tau_kp, tau_kq, 
    #                 possibilities, 32, known_bits_p, known_bits_q, known_bits_d, known_bits_dp, known_bits_dq, verbose, counter)

if __name__ == "__main__":
    main()