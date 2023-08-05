import numpy as np
# import crypto
import cv2
import sys

# sys.modules['Crypto'] = crypto


# from Crypto.Cipher import AES
import binascii


def one_dim_kmeans(inputs):
    e_tol = 10 ** (-6)

    center = [inputs.min(), inputs.max()]  # 1. 初始化中心点

    for i in range(300):
        threshold = (center[0] + center[1]) / 2
        is_class01 = inputs > threshold  # 2. 检查所有点与这k个点之间的距离，每个点归类到最近的中心
        center = [inputs[~is_class01].mean(), inputs[is_class01].mean()]  # 3. 重新找中心点
        if np.abs((center[0] + center[1]) / 2 - threshold) < e_tol:  # 4. 停止条件
            threshold = (center[0] + center[1]) / 2
            break

    is_class01 = inputs > threshold

    return is_class01


# %%


# %%
# 使bit类数据的0和1数量相同
def blance_bit():
    pass


def str_encrypt(text, password):
    text = text.encode('utf-8')
    # cryptor = AES.new(key='{:0<16}'.format(password).encode('utf-8'),
    #                   mode=AES.MODE_ECB)  # key 长度必须是16,24,32 长度的 byte 格式
    #
    # ciphertext_tmp = cryptor.encrypt(text + b' ' * (16 - len(text) % 16))  # 明文的长度必须是16的整数倍
    ciphertext_tmp = text
    ciphertext_tmp_hex = ciphertext_tmp.hex()  # 转16进制文本

    ciphertext_bin = bin(int(ciphertext_tmp_hex, 16))[2:]  # 转二进制

    ciphertext_arr = (np.array(list(ciphertext_bin)) == '1')

    return ciphertext_arr, len(ciphertext_arr)


def str_decrypt(ciphertext_arr, password):
    # ciphertext_bin = ''.join(['1' if i else '0' for i in ciphertext_arr])
    # ciphertext = hex(int(ciphertext_bin, base=2))[2:]
    # text = AES.new(key='{:0<16}'.format(password).encode('utf-8'), mode=AES.MODE_ECB) \
    #     .decrypt(binascii.a2b_hex(ciphertext)).decode('utf-8')

    byte = ''.join((np.round(ciphertext_arr)).astype(np.int).astype(np.str))
    wm = bytes.fromhex(hex(int(byte, base=2))[2:]).decode('utf-8')
    return wm


def recovery(ori_img, attacked_img, outfile_name='./recoveried.png', rate=0.95):
    img = cv2.imread(ori_img)
    img2 = cv2.imread(attacked_img)

    height = img.shape[0]
    width = img.shape[1]
    # Initiate SIFT detector
    orb = cv2.ORB_create(128)
    MIN_MATCH_COUNT = 10
    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    des1 = np.float32(des1)
    des2 = np.float32(des2)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < rate * n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
        out = cv2.warpPerspective(img2, M, (width, height))  # 先列后行
        cv2.imwrite(outfile_name, out)
        print("还原截屏攻击成功")
        return True
    else:
        print("无法还原")
        return False


if __name__ == "__main__":
    text = '加密文本。test!'
    password = 20190808

    ciphertext_arr, len_ciphertext_arr = str_encrypt(text, password)

    text = str_decrypt(ciphertext_arr, password)

    print(text)
