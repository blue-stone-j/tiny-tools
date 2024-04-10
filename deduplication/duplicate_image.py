import os
import hashlib
from PIL import Image
import json

def hash_image(image_path):
    """计算图片的哈希值"""
    with Image.open(image_path) as img:
        # 将图片转换为字节串
        img_bytes = img.tobytes()
        hash_obj = hashlib.md5(img_bytes)
        return hash_obj.hexdigest()

def find_images(root_dir, extensions=('.jpg', '.jpeg', '.png', '.gif')):
    """递归查找指定文件夹内的所有图片文件"""
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(extensions):
                yield os.path.join(root, file)

def main(root_dir, output_file):
    hash_map = {}
    for image_path in find_images(root_dir):
        image_hash = hash_image(image_path)
        if image_hash in hash_map:
            hash_map[image_hash].append(image_path)
        else:
            hash_map[image_hash] = [image_path]

    # 删除没有重复的图片的键值对
    hash_map = {hash_val: paths for hash_val, paths in hash_map.items() if len(paths) > 1}

    # 写入文件
    with open(output_file, 'w') as f:
        json.dump(hash_map, f, indent=4)

# 请替换下面的路径
root_directory = './ori'
output_filename = 'duplicate_images.json'
main(root_directory, output_filename)

