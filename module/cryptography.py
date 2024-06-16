import numpy as np

# 加密影像
def encrypt_image_3d(plain_image, sbox, chaotic_mask):
    encrypted_image = np.zeros_like(plain_image, dtype=np.uint16)
    
    for i in range(plain_image.shape[0]):
        for j in range(plain_image.shape[1]):
            for k in range(plain_image.shape[2]):       
                I_i = plain_image[i, j, k] # 取得原始像素值
                M_i = chaotic_mask[i, j, k] # 取得混沌遮罩值 
                M_i_prime = int(bin(M_i)[2:][::-1], 2) % 256  # 翻轉二進位表示
                
                encrypted_pixel = sbox[M_i_prime ^ sbox[M_i ^ sbox[I_i]]] # 透過動態S-box進行像素替換
                encrypted_image[i, j, k] = encrypted_pixel
    return encrypted_image


def decrypt_image_3d(encrypted_image, sbox, chaotic_mask):
    decrypted_image = np.zeros_like(encrypted_image, dtype=np.uint8) # 初始化解密影像 (使用uint8表示像素值)

    inv_sbox = np.zeros_like(sbox) # 計算S-box的反向查找表
    for i in range(len(sbox)):
        inv_sbox[sbox[i]] = i

    for i in range(encrypted_image.shape[0]):
        for j in range(encrypted_image.shape[1]):
            for k in range(encrypted_image.shape[2]):
                C_i = encrypted_image[i, j, k]
                
                M_i = chaotic_mask[i, j, k] # 取得混沌遮罩值
                M_i_prime = int(bin(M_i)[2:][::-1], 2) % 256 # 翻轉二進位表示

                S_C_i = inv_sbox[C_i] # 取得密文像素值的反向查找表值
                inner_value = M_i_prime ^ S_C_i
                S_inner_value = inv_sbox[inner_value]
                middle_value = M_i ^ S_inner_value
                I_i = inv_sbox[middle_value]

                decrypted_image[i, j, k] = I_i # 將解密後的像素值填入解密影像
    return decrypted_image


if __name__ == "__main__":
    print("This is a module file, import it to use.")