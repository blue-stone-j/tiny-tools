from PIL import Image
import os
import numpy as np

def dhash(image, hash_size=8):
    """计算图片的差异哈希值"""
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.LANCZOS)
    pixels = list(image.getdata())
    difference = [pixels[i] > pixels[i+1] for i in range(hash_size * hash_size)]
    decimal_value = 0
    hash_string = ""
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hash_string += str(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return hash_string

def hamming_distance(hash1, hash2):
    """计算两个哈希值之间的汉明距离"""
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

def find_images(root_dir, extensions=('.jpg', '.jpeg', '.png', '.gif')):
    """递归查找指定文件夹内的所有图片文件"""
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(extensions):
                yield os.path.join(root, file)

def group_similar_images(root_dir, distance_threshold=5):
    """将相似图片分组"""
    images = list(find_images(root_dir))
    hashes = {img: dhash(Image.open(img)) for img in images}
    groups = []
    
    for img, img_hash in hashes.items():
        found = False
        for group in groups:
            if hamming_distance(hashes[group[0]], img_hash) <= distance_threshold:
                group.append(img)
                found = True
                break
        if not found:
            groups.append([img])
    
    # 只返回包含多于一个元素的分组
    similar_groups = [group for group in groups if len(group) > 1]
    return similar_groups

# 递归查找并分组相似图片
root_directory = './ori' # 请替换为你的图片目录
similar_images_groups = group_similar_images(root_directory)

# 如果找到相似图片，将分组结果保存到文本文件中
if similar_images_groups:
    output_file = 'similar_images_groups.txt'
    with open(output_file, 'w') as f:
        for group in similar_images_groups:
            f.write("\n".join(group) + "\n\n")
    print(f"分组结果已保存到 {output_file}")
else:
    print("没有找到相似的图片，不保存结果。")
