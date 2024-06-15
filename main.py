import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from module.util import initialize_prng, generate_chaotic_mask_3d, construct_sbox, fisher_yates_shuffle, baker_map
from module.cryptography import encrypt_image_3d, decrypt_image_3d


PIXEL_RANGE = 4096 # 像素值範圍
SEED_LEN = 16
PLAIN_IMAGE_PATH = "./fig/figure.jpg"


def get_image_data(plain_image):
    image_size = (plain_image.size[1], plain_image.size[0], 3)
    image_array = np.array(plain_image.resize((image_size[1], image_size[0])))
    
    # hint : 若圖像為灰度，則轉為三通道
    if len(image_array.shape) == 2:
        image_array = np.stack((image_array,)*3, axis=-1)

    prng = initialize_prng(SEED_LEN)  # PRNG 初始化
    sbox = construct_sbox(prng, PIXEL_RANGE) # 建立S-Box
    
    chaotic_seed = prng.random(size=SEED_LEN)
    chaotic_mask_3d = generate_chaotic_mask_3d(chaotic_seed, image_size)
    
    return image_array, sbox, chaotic_mask_3d

def display_image(plain_image, encrypted_image_display, decrypted_image):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Create a figure and subplots

    images = [plain_image, encrypted_image_display, decrypted_image]
    titles = ["Plain Image", "Encrypted Image", "Decrypted Image"]

    for ax, img, title in zip(axes, images, titles):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')

    print("Displaying results...")
    plt.show()




if __name__ == "__main__":
    plain_image = Image.open(PLAIN_IMAGE_PATH)
    image_array, sbox, chaotic_mask_3d = get_image_data(plain_image)
    print("Image data loaded successfully.")
    
    # 加密圖像
    encrypted_image = encrypt_image_3d(image_array, sbox, chaotic_mask_3d)
    print("Image encrypted successfully.")
    
    # hint : 將加密影像資料歸一化到 [0, 1]
    encrypted_image_display = (encrypted_image / encrypted_image.max())
    
    # 解密圖像
    decrypted_image = decrypt_image_3d(encrypted_image, sbox, chaotic_mask_3d)
    print("Image decrypted successfully.")
    
    # 顯示結果
    display_image(image_array, encrypted_image_display, decrypted_image)
    