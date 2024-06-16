import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from module.cryptography import encrypt_image_3d

PIXEL_RANGE = 4096 # 像素值範圍

# 計算圖像的熵
def calculate_entropy(image):
    hist, _ = np.histogram(image.flatten(), bins=4096, range=(0, 4095))
    prob = hist / hist.sum()
    entropy = -np.sum([p * np.log2(p) for p in prob if p != 0])
    return entropy

# 交叉相關性和空間自相關性
## 計算圖像的交叉相關性
def cross_correlation(image1, image2):
    return np.corrcoef(image1.flatten(), image2.flatten())[0, 1]

## 計算圖像的空間自相關性
def spatial_autocorrelation(image):
    autocorr_h = np.corrcoef(image[:, :-1].flatten(), image[:, 1:].flatten())[0, 1]
    autocorr_v = np.corrcoef(image[:-1, :].flatten(), image[1:, :].flatten())[0, 1]
    autocorr_d = np.corrcoef(image[:-1, :-1].flatten(), image[1:, 1:].flatten())[0, 1]
    return autocorr_h, autocorr_v, autocorr_d


# 直方圖和卡方檢驗
def chi_square_test(image):
    hist, _ = np.histogram(image.flatten(), bins=4096, range=(0, 4095))
    expected_freq = np.ones(4096) * (hist.sum() / 4096)  # 確保期望頻率和觀察頻率總和一致
    chi2, p = chisquare(hist, expected_freq)
    return chi2, p

# 計算 NPCR 以及 UACI
def calculate_npcr(img1, img2):
    """ Calculate Normalized Pixel Change Rate (NPCR) """
    if img1.shape != img2.shape:
        raise ValueError("Images must have the same dimensions.")

    total_pixels = img1.size
    diff_pixels = np.count_nonzero(img1 != img2)
    npcr_rate = diff_pixels / total_pixels
    return npcr_rate*100

def calculate_uaci(img1, img2):
    """ Calculate Unified Average Change Intensity (UACI) """
    if img1.shape != img2.shape:
        raise ValueError("Images must have the same dimensions.")
    
    uaci_value = np.sum(np.abs(img1 - img2)) / (img1.size * 255)
    return uaci_value

def measure_key_sensitivity(encrypted_image, image_array, sbox, chaotic_mask_3d):
    encrypted_image_2 = encrypt_image_3d(image_array, sbox, chaotic_mask_3d)
    npcr = calculate_npcr(encrypted_image, encrypted_image_2)
    uaci = calculate_uaci(encrypted_image, encrypted_image_2)
    return npcr, uaci

def modify_image_pixels(image_array, percentage):
    height, width, channels = image_array.shape

    # 計算要修改的區域大小
    area_size = int(np.sqrt(height * width * percentage))  # 使用平方根來確定區域大小
    area_size = max(area_size, 1)  # 確保區域大小至少為1

    # 隨機選擇區域的左上角位置
    start_row = np.random.randint(0, height - area_size + 1)
    start_col = np.random.randint(0, width - area_size + 1)

    # 設置灰色值
    gray_value = np.random.randint(0, 256)

    # 修改像素值
    modified_image = np.copy(image_array)
    modified_image[start_row:start_row+area_size, start_col:start_col+area_size, :] = gray_value

    return modified_image


if __name__ == "__main__":
    print("Warning: This is a module file, import it to use.")