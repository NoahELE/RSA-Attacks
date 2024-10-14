import gmpy2
import random
import time

KNOWN_BIT_PERCENTAGE = 70

class KnownBit:
    def __init__(self, position, value):
        self.position = position
        self.value = value

# 读取并转换RSA密钥的组件
def read_and_convert_component(component, file):
    for line in file:
        if '=' in line:
            hex_str = line.split('=')[1].strip()  # 跳过"="并获取十六进制数
            component = gmpy2.mpz(hex_str, 16)
            return component

# 降级RSA组件的已知位
def degrade_component(component, filename):
    total_bits = component.bit_length()  # 获取总位数
    known_bit_count = (total_bits * KNOWN_BIT_PERCENTAGE) // 100
    all_bits = [KnownBit(i, -1) for i in range(total_bits)]  # 初始化所有位为未知（-1）

    # 创建所有位的索引列表并随机打乱
    indices = list(range(total_bits))
    random.seed(time.time())
    random.shuffle(indices)

    # 选择前known_bit_count个已知位
    for i in range(known_bit_count):
        bit_value = gmpy2.bit_test(component, indices[i])
        all_bits[indices[i]].value = int(bit_value)

    # 将位信息写入文件
    with open(filename, "w") as file:
        for bit in all_bits:
            file.write(f"{bit.position} {bit.value}\n")

# 主函数
def main():
    rsa_components = ["n", "e", "d", "p", "q", "dp", "dq", "qp"]
    rsa_values = {}

    # 读取hexa-RSA-Key.txt文件并转换组件
    with open("hexa-RSA-Key.txt", "r") as rsakey_file:
        for component in rsa_components:
            rsa_values[component] = gmpy2.mpz(0)
            rsa_values[component] = read_and_convert_component(rsa_values[component], rsakey_file)

    # 分别降级每个组件并保存降级信息
    degrade_component(rsa_values["n"], "known_bits_n.txt")
    degrade_component(rsa_values["e"], "known_bits_e.txt")
    degrade_component(rsa_values["d"], "known_bits_d.txt")
    degrade_component(rsa_values["p"], "known_bits_p.txt")
    degrade_component(rsa_values["q"], "known_bits_q.txt")
    degrade_component(rsa_values["dp"], "known_bits_dp.txt")
    degrade_component(rsa_values["dq"], "known_bits_dq.txt")
    degrade_component(rsa_values["qp"], "known_bits_qp.txt")

if __name__ == "__main__":
    main()
