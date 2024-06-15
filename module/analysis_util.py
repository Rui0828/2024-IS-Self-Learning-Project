import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from PIL import Image


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


if __name__ == "__main__":
    print("Warning: This is a module file, import it to use.")
 