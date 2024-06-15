import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from module.util import initialize_prng, generate_chaotic_mask_3d, construct_sbox, fisher_yates_shuffle, baker_map
from module.cryptography import encrypt_image_3d, decrypt_image_3d

plain_image = Image.open("./fig/figure.jpg")

image_size = (plain_image.size[1], plain_image.size[0], 3)

# resize圖像大小為混沌遮罩的大小
resized_image = plain_image.resize((image_size[1], image_size[0]))

image_array = np.array(resized_image)

if len(image_array.shape) == 2:
    image_array = np.stack((image_array,)*3, axis=-1)

# 初始化混沌遮罩的种子
prng = initialize_prng(16)  # PRNG 初始化 seed_length = 16
chaotic_seed = prng.random(size=16)
print("Random numbers:", chaotic_seed)

# 初始化S-Box
pixel_range = 4096 # 8-bit像素範圍
sbox = construct_sbox(prng, pixel_range) # 建立S-Box

# 生成三维混沌遮罩
chaotic_mask_3d = generate_chaotic_mask_3d(chaotic_seed, image_size)

# 加密原始图像
encrypted_image = encrypt_image_3d(image_array, sbox, chaotic_mask_3d)

# hint : 將加密影像資料歸一化到 [0, 1]
encrypted_image_display = (encrypted_image / encrypted_image.max())

# 解密加密图像
decrypted_image = decrypt_image_3d(encrypted_image, sbox, chaotic_mask_3d)

#維持寬高比顯示
fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Create a figure and subplots

images = [plain_image, encrypted_image_display, decrypted_image]
titles = ["Plain Image", "Encrypted Image", "Decrypted Image"]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap='gray')
    ax.set_title(title)
    ax.axis('off')

plt.show()