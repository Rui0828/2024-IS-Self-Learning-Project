from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from main import get_image_data
from module.cryptography import encrypt_image_3d
from module.analysis_util import calculate_entropy, cross_correlation, spatial_autocorrelation, chi_square_test, calculate_npcr, calculate_uaci, measure_key_sensitivity, modify_image_pixels


PIXEL_RANGE = 4096 # 像素值範圍
SEED_LEN = 16
PLAIN_IMAGE_PATH = "./fig/5.jpg"


# plot image and histogram
def display_analysis_results(plain_image, encrypted_image):
    fig, axs = plt.subplots(1, 4, figsize=(15, 5))
    fig.suptitle("Image and Histogram Comparison")

    # Normalize encrypted image data to [0, 1]
    encrypted_image_display = (encrypted_image / encrypted_image.max() * 255).astype(np.uint8)

    axs[0].set_title("Plain Image")
    axs[0].imshow(plain_image, cmap='gray')
    axs[0].axis('off')
    
    axs[1].set_title("Plain Image Histogram")
    axs[1].hist(np.array(plain_image).flatten(), bins=4096, range=(0, 4095), color='blue')
    
    axs[2].set_title("Encrypted Image")
    axs[2].imshow(encrypted_image_display, cmap='gray')
    axs[2].axis('off')
    
    axs[3].set_title("Encrypted Image Histogram")
    axs[3].hist(np.array(encrypted_image).flatten(), bins=4096, range=(0, 4095), color='blue')

    plt.tight_layout()
    print("Displaying results...")
    plt.show()



if __name__ == "__main__":
    plain_image = Image.open(PLAIN_IMAGE_PATH)
    image_array, sbox, chaotic_mask_3d, sbox_2, chaotic_mask_3d_2 = get_image_data(plain_image)
    print("Image data loaded successfully.")
    
    # 加密圖像
    encrypted_image = encrypt_image_3d(image_array, sbox, chaotic_mask_3d)
    encrypted_array = np.array(encrypted_image)
    print("Image encrypted successfully.")

    print("\n------------- Analysis Result -------------")
    # 計算圖像的熵
    entropy = calculate_entropy(image_array)
    print("Entropy:", entropy)
    
    # 計算圖像的交叉相關性
    cross_corr = cross_correlation(image_array, encrypted_array)
    
    # 計算圖像的空間自相關性
    autocorr_h, autocorr_v, autocorr_d = spatial_autocorrelation(encrypted_array)
    print("Horizontal spatial autocorrelation:", autocorr_h)
    print("Vertical spatial autocorrelation:", autocorr_v)
    print("Diagonal spatial autocorrelation:", autocorr_d)
    
    # 直方圖和卡方檢驗
    chi2, p = chi_square_test(encrypted_array)
    print("Chi-square value:", chi2)
    print("p-value:", p)
    print("------------------------------------------")
    
    # 顯示加密前後的圖片和直方圖
    display_analysis_results(image_array, encrypted_image)
    