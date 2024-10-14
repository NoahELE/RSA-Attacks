import gmpy2

def flip_bits_and_compute_d(orig_filename, mod_filename):
    try:
        # 打开原始文件，查找'd='行并提取d的值
        with open(orig_filename, "r") as orig_file:
            d = None
            for line in orig_file:
                if line.startswith("d="):
                    d_str = line[2:].strip()  # 跳过"d="并获取数字部分
                    d = gmpy2.mpz(d_str)  # 假设'd'是十进制的
                    break
            
            if d is None:
                raise ValueError("未能在原始文件中找到'd'值。")

        # 打开修改文件，读取需要翻转的位
        with open(mod_filename, "r") as mod_file:
            for line in mod_file:
                position, value = map(int, line.split())
                if value == -1:  # 仅在需要翻转位时操作
                    if gmpy2.bit_test(d, position):  # 如果当前位是1，则翻转为0
                        d = gmpy2.bit_clear(d, position)
                    else:  # 翻转为1
                        d = gmpy2.bit_set(d, position)

        # 打印最终的d值
        print(f"Final value of d: {d}")

    except FileNotFoundError as e:
        print(f"文件打开错误: {e}")
    except ValueError as e:
        print(f"数据处理错误: {e}")

def main():
    flip_bits_and_compute_d("RSA-Key.txt", "known_bits_d.txt")

if __name__ == "__main__":
    main()
