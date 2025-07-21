
import ruamel.yaml

'''
load, change, dump yaml file
'''
# load yaml file
# ruamel.yaml is a YAML parser/emitter that supports round-trip preservation of comments and formatting
# It is a drop-in replacement for PyYAML, but with more features and better support
yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
with open('params.yaml') as f:
    config = yaml.load(f)

# cache comments
# ruamel.yaml does not preserve comments by default, so we need to handle them manually
# Here we assume comments start with '#'
comments = {} 
for k,v in config.items():
    if k.startswith('#'):
        comments[k] = v
        del config[k]

# edit
config['utm_zone']=50 # add or edit a key-value pair
print('utm_zone: ',config['utm_zone']) # print the changed value

# data["pos"] is a list of dictionaries
for item in config.get("pos", []):
    if item.get("key") == "x":
        value = item.get("value")

# write to new file
with open('test.yaml','w') as f:
  yaml.indent(mapping=2, sequence=4, offset=2)
  yaml.dump(config, f)
  for k,v in comments.items():
      f.write(f'{k}: {v}\n')

'''
create a new yaml file
'''

# Step 1: Create empty data
data = {}

# Step 2: Add values progressively
data['project'] = 'VisualMark'
data['version'] = 2.1
data['enabled'] = True
data['dependencies'] = ['pcl', 'opencv', 'qt']

# You may also add nested dictionaries step by step
data['config'] = {}
data['config']['use_gpu'] = False
data['config']['batch_size'] = int(8)
data['config']['thresholds'] = [0.2, 0.4, 0.6]

# Step 3: Dump to YAML file
with open('output.yaml', 'w') as file:
    yaml.dump(data, file, default_flow_style=False, sort_keys=False)

print("YAML file 'output.yaml' created successfully.")