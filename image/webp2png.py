# convert image from web to png using Python and Pillow

import os
from PIL import Image

def convert_webp_to_png(directory):
    # 遍历指定目录及其所有子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".webp"):
                webp_path = os.path.join(root, file)
                png_path = os.path.join(root, file[:-5] + ".png")

                # 尝试将WEBP转换为PNG
                try:
                    with Image.open(webp_path) as image:
                        image.save(png_path, "PNG")
                    
                    # 如果转换成功，删除原WEBP文件
                    os.remove(webp_path)
                    print(f"Converted and removed: {webp_path}")
                except Exception as e:
                    print(f"Failed to convert {webp_path}: {e}")

# 使用函数，并指定要遍历的根目录
convert_webp_to_png("/path/to/directory")

