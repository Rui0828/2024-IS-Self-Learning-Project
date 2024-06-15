from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import numpy as np

# 初始化
## Create PRNG
def initialize_prng(seed_length):
    aes_key = get_random_bytes(AES.block_size)  # 使用AES金鑰產生隨機序列
    random_sequence = generate_random_sequence(aes_key, seed_length)

    prng = np.random.default_rng(int.from_bytes(random_sequence, byteorder='big'))  # 使用隨機序列作為種子初始化PRNG
    return prng


## Generate random sequence
def generate_random_sequence(key, sequence_length):
    cipher = AES.new(key, AES.MODE_CBC, IV=get_random_bytes(AES.block_size)) # 建立加密器
    random_sequence = bytearray()

    while len(random_sequence) < sequence_length:
        block = cipher.encrypt(get_random_bytes(AES.block_size)) # 使用AES加密器加密一個區塊
        random_sequence.extend(block)

    return bytes(random_sequence[:sequence_length]) # 裁剪為所需的長度


# 實作S-Box、混沌映射&遮罩
## Fisher-Yates shuffle 演算法
def fisher_yates_shuffle(arr, rng):
    for i in range(len(arr) - 1, 0, -1):
        j = rng.integers(0, i + 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


## S-Box
def construct_sbox(seed, pixel_range):
    rng = np.random.default_rng(seed) # 使用seed整數作為隨機數種子創建PRNG
    sbox = np.arange(pixel_range, dtype=np.uint16)
    sbox = fisher_yates_shuffle(sbox, rng)
    return sbox


## 定義Baker映射
def baker_map(x, y, a, b):
    x_new = a * (x + y) % 1
    y_new = b * (x - y) % 1
    return x_new, y_new

## 生成3D混沌遮罩
def generate_chaotic_mask_3d(seed, image_size, a=0.921064, b=0.040442):
    chaotic_mask = np.zeros(image_size, dtype=np.uint16)  # 使用16位元表示
    rng = np.random.default_rng(int.from_bytes(seed, byteorder='big'))
    x = rng.random()
    y = rng.random()
    for i in range(image_size[0]):
        for j in range(image_size[1]):
            for k in range(image_size[2]):
                x, y = baker_map(x, y, a, b)
                chaotic_mask[i, j, k] = rng.integers(0, 4096)
    return chaotic_mask





if __name__ == "__main__":
    print("--------------- Util module test ---------------")
    print("Warning: This is a module file, import it to use.")
    print("------------------------------------------------")
    print("PRNG initialization test:")
    prng = initialize_prng(16)
    random_numbers = prng.random(size=10) # 產生10個隨機數
    print("Random numbers:", random_numbers)
    print("------------------------------------------------")
    print("S-Box construction test:")
    pixel_range = 4096 # 8-bit像素範圍
    sbox = construct_sbox(prng, pixel_range) # 建立S-Box
    print("S-Box:", sbox)
    print("------------------------------------------------")
    chaotic_mask_3d = generate_chaotic_mask_3d(random_numbers, (512, 512, 3)) # 生成3D混沌遮罩
    print("3D chaotic mask shape:", chaotic_mask_3d.shape)
    print("------------------------------------------------")
    print("---------  Util module test completed ----------")