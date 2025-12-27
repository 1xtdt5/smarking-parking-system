import os
import shutil
import random

# 设置随机种子确保可重复性
random.seed(42)

# 获取所有图像文件
all_images = [f for f in os.listdir('images') if f.endswith('.png')]
random.shuffle(all_images)

# 计算划分数量
total = len(all_images)
train_count = int(total * 0.7)
val_count = int(total * 0.2)
test_count = total - train_count - val_count

# 划分数据集
train_images = all_images[:train_count]
val_images = all_images[train_count:train_count+val_count]
test_images = all_images[train_count+val_count:]

# 复制函数
def copy_files(image_list, split_type):
    for filename in image_list:
        # 复制图像
        src_img = os.path.join('images', filename)
        dst_img = os.path.join('dataset', 'images', split_type, filename)
        shutil.copy2(src_img, dst_img)
        
        # 复制对应的标注文件
        label_filename = os.path.splitext(filename)[0] + '.txt'
        src_label = os.path.join('labels', label_filename)
        dst_label = os.path.join('dataset', 'labels', split_type, label_filename)
        if os.path.exists(src_label):
            shutil.copy2(src_label, dst_label)
        else:
            print(f"Warning: Label file not found for {filename}")

# 执行复制
print(f"Total images: {total}")
print(f"Training images: {len(train_images)}")
print(f"Validation images: {len(val_images)}")
print(f"Test images: {len(test_images)}")

print("Copying training files...")
copy_files(train_images, 'train')

print("Copying validation files...")
copy_files(val_images, 'val')

print("Copying test files...")
copy_files(test_images, 'test')

print("Dataset splitting completed successfully!")