
import ruamel.yaml

# 读取YAML文件
yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
with open('params.yaml') as f:
    config = yaml.load(f)

# 处理注释
comments = {} 
for k,v in config.items():
    if k.startswith('#'):
        comments[k] = v
        del config[k]

# 处理文件
config['utm_zone']=50 # 添加或修改参数
print('square_size: ',config['square_num']) # 输出

# 写入新文件
with open('test.yaml','w') as f:
  yaml.indent(mapping=2, sequence=4, offset=2)
  yaml.dump(config, f)
  for k,v in comments.items():
      f.write(f'{k}: {v}\n')

