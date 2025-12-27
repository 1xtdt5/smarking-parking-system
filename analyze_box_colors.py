import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取掩码图像
mask_path = 'boxes/0.png'
img = cv2.imread(mask_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 显示图像信息
print('图像尺寸:', img.shape)
print('颜色通道:', img.shape[2] if len(img.shape) > 2 else 1)

# 提取RGB通道
red_channel = img_rgb[:, :, 0]
green_channel = img_rgb[:, :, 1]
blue_channel = img_rgb[:, :, 2]

# 计算颜色直方图
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.hist(red_channel.ravel(), bins=256, color='red', alpha=0.7)
plt.title('Red Channel')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.subplot(132)
plt.hist(green_channel.ravel(), bins=256, color='green', alpha=0.7)
plt.title('Green Channel')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.subplot(133)
plt.hist(blue_channel.ravel(), bins=256, color='blue', alpha=0.7)
plt.title('Blue Channel')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('color_histogram.png')
plt.close()

print('颜色直方图已保存为 color_histogram.png')

# 寻找可能的蓝色和红色像素值
# 蓝色通常是低红、低绿、高蓝
# 红色通常是高红、低绿、低蓝

# 提取蓝色区域（蓝通道值高，红和绿通道值低）
blue_mask = (blue_channel > 200) & (red_channel < 100) & (green_channel < 100)
blue_pixels = img_rgb[blue_mask]

# 提取红色区域（红通道值高，绿和蓝通道值低）
red_mask = (red_channel > 200) & (green_channel < 100) & (blue_channel < 100)
red_pixels = img_rgb[red_mask]

print('\n蓝色像素统计:')
if len(blue_pixels) > 0:
    print(f'数量: {len(blue_pixels)}')
    print(f'平均RGB值: {np.mean(blue_pixels, axis=0)}')
    print(f'最小RGB值: {np.min(blue_pixels, axis=0)}')
    print(f'最大RGB值: {np.max(blue_pixels, axis=0)}')
else:
    print('未找到蓝色像素')

print('\n红色像素统计:')
if len(red_pixels) > 0:
    print(f'数量: {len(red_pixels)}')
    print(f'平均RGB值: {np.mean(red_pixels, axis=0)}')
    print(f'最小RGB值: {np.min(red_pixels, axis=0)}')
    print(f'最大RGB值: {np.max(red_pixels, axis=0)}')
else:
    print('未找到红色像素')

# 尝试不同的阈值来提取蓝色和红色区域
print('\n尝试不同阈值提取颜色区域:')

# 蓝色阈值范围（BGR格式，因为OpenCV默认使用BGR）
lower_blue = np.array([150, 0, 0])
upper_blue = np.array([255, 100, 100])

# 红色阈值范围（BGR格式）
lower_red = np.array([0, 0, 150])
upper_red = np.array([100, 100, 255])

# 转换为HSV色彩空间可能更容易检测颜色
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# HSV中蓝色的范围
lower_blue_hsv = np.array([100, 150, 50])
upper_blue_hsv = np.array([130, 255, 255])

# HSV中红色的范围（红色有两个范围）
lower_red_hsv1 = np.array([0, 150, 50])
upper_red_hsv1 = np.array([10, 255, 255])
lower_red_hsv2 = np.array([160, 150, 50])
upper_red_hsv2 = np.array([180, 255, 255])

# 提取蓝色区域
blue_mask_bgr = cv2.inRange(img, lower_blue, upper_blue)
blue_mask_hsv = cv2.inRange(hsv, lower_blue_hsv, upper_blue_hsv)

# 提取红色区域
red_mask_bgr = cv2.inRange(img, lower_red, upper_red)
red_mask_hsv1 = cv2.inRange(hsv, lower_red_hsv1, upper_red_hsv1)
red_mask_hsv2 = cv2.inRange(hsv, lower_red_hsv2, upper_red_hsv2)
red_mask_hsv = cv2.bitwise_or(red_mask_hsv1, red_mask_hsv2)

print(f'BGR蓝色像素数量: {np.sum(blue_mask_bgr > 0)}')
print(f'HSV蓝色像素数量: {np.sum(blue_mask_hsv > 0)}')
print(f'BGR红色像素数量: {np.sum(red_mask_bgr > 0)}')
print(f'HSV红色像素数量: {np.sum(red_mask_hsv > 0)}')

# 保存检测结果
cv2.imwrite('blue_mask_bgr.png', blue_mask_bgr)
cv2.imwrite('blue_mask_hsv.png', blue_mask_hsv)
cv2.imwrite('red_mask_bgr.png', red_mask_bgr)
cv2.imwrite('red_mask_hsv.png', red_mask_hsv)

print('\n颜色掩码已保存为PNG文件')