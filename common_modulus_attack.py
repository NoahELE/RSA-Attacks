class CommonModulusAttack:
    def __init__(self):
        pass

    def rsa_encrypt(self, e, n, m):
        if m >= n:
            raise ValueError("m should less than n")
        
        c = pow(m, e, n)
        
        return c

    def extended_gcd(self, a, b):
        if b == 0:
            return 1, 0
        else:
            x1, y1 = self.extended_gcd(b, a % b)
            x = y1
            y = x1 - (a // b) * y1
            return x, y
        
    def common_modulus_attack(self, c1, e1, c2, e2, n):
        s1, s2 = self.extended_gcd(e1, e2)
        m = (pow(c1, s1, n) * pow(c2, s2, n)) % n
        return m


def run_test_case(testcase):
    comm_mod_att = CommonModulusAttack()

    e1 = testcase["e1"]
    e2 = testcase["e2"]
    n = testcase["n"]
    m_original = testcase["m_original"]
    c1 = comm_mod_att.rsa_encrypt(e1, n, m_original)
    c2 = comm_mod_att.rsa_encrypt(e2, n, m_original)
    print(f"c1: {c1}, c2: {c2}")

    m_recovered = comm_mod_att.common_modulus_attack(c1, e1, c2, e2, n)
    print(f"Recovered message m: {m_recovered}, Original message m: {m_original}")
    print(f"m_recovered equal to m_original: {m_recovered == m_original}")


if __name__ == "__main__":
    Test_1 = {"n" : 221, "m_original" : 87, "e1" : 7, "e2" : 19}
    Test_2 = {"n" : 10000000000000000000, "m_original" : 1234567890123456789, "e1" : 7, "e2" : 19}
    Test_3 = {"n" : 987654321987654321987654321987654321, "m_original" : 98765432123456789, "e1" : 17, "e2" : 23}

    run_test_case(Test_1)
    run_test_case(Test_2)
    run_test_case(Test_3)