'''
open a csv file, then replace all num 7 with 0 and replace other num with 1
'''

import csv
import re

# 检测字符串是否为数字（整数或小数）
def is_number(s):
    return re.match(r'^-?\d+(?:\.\d+)?$', s) is not None

# 输入和输出文件路径
input_csv_path = 'ori.csv'
output_csv_path = 'out.csv'

# 读取 CSV 文件
with open(input_csv_path, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    data = list(reader)

# 数据处理：将数字7替换为0，其他数字替换为1
processed_data = []
for row in data:
    new_row = []
    for item in row:
        if is_number(item):  # 检测是否为数字
            # 处理数字，包括整数和小数
            if float(item) == 7:
                new_item = '0'
            else:
                new_item = '1'
        else:
            new_item = item  # 非数字保持不变
        new_row.append(new_item)
    processed_data.append(new_row)

# 将处理后的数据写入新的 CSV 文件
with open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(processed_data)

