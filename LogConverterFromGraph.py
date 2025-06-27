import re
from collections import defaultdict

# Load the DOT file content
with open("./data/JpetStore/assemblyOperationDependencyGraph_category.dot") as f:
    dot_data = f.read()
    
    

node_class_mapping = {}
current_class = None

def process_depNode_label_to_extract_metadata(node):
    label = node['label']
    label_clean = label.replace("\\n", "").strip()
    
    # Extract method name if present
    # Updated regex to match method names with () or (..)
    method_match = re.match(r'(?:<([^>]+)>|(\w+\(\.*\)))', label_clean)
    if method_match:
        raw_methodname = method_match.group(1) if method_match.group(1) else method_match.group(2)
        # Clean up method name by removing '()', '(..)', etc.
        node['methodname'] = raw_methodname.replace('()', '').replace('(..)', '')
        label_clean = label_clean[method_match.end():].replace('()', '').replace('(..)', '')
        label_clean = label_clean.strip()  # Remove any leading/trailing whitespace

    # Extract min, avg, max, total values
    for part in label_clean.split(','):
        if ':' in part:
            key, value = part.split(':', 1)
            node[key.strip()] = value.strip()
    


for line in dot_data.splitlines():
    class_match = re.search(r'label\s*=\s*"<<assembly component>>\\n@[\d]+:(.*?)"', line)
    if class_match:
        current_class = class_match.group(1).strip()

    node_match = re.match(r'"(depNode_\d+)"\s+\[label="([^"]+)"', line)
    if node_match and current_class:
        node_id, label = node_match.groups()
        label_clean = label.replace("\\n", " ").replace("\n", " ").strip()
        node_class_mapping[node_id] = {
            "label": label_clean,
            "class": current_class
        }
        process_depNode_label_to_extract_metadata(node_class_mapping[node_id])


# node_metadata = {}

# n = re.findall(r'"(depNode_\d+)"\s+\[label="([^"]+?)"', dot_data, re.DOTALL)

# for node, label in re.findall(r'"(depNode_\d+)"\s+\[label="([^"]+?)"', dot_data, re.DOTALL):
#     label_clean = label.replace("\\n", "").strip()
#     metadata = {}
    
#     # Extract method name if present
#     # Updated regex to match method names with () or (..)
#     method_match = re.match(r'(?:<([^>]+)>|(\w+\(\.*\)))', label_clean)
#     if method_match:
#         raw_methodname = method_match.group(1) if method_match.group(1) else method_match.group(2)
#         # Clean up method name by removing '()', '(..)', etc.
#         metadata['methodname'] = raw_methodname.replace('()', '').replace('(..)', '')
#         label_clean = label_clean[method_match.end():].replace('()', '').replace('(..)', '')
#         label_clean = label_clean.strip()  # Remove any leading/trailing whitespace

#     # Extract min, avg, max, total values
#     for part in label_clean.split(','):
#         if ':' in part:
#             key, value = part.split(':', 1)
#             metadata[key.strip()] = value.strip()

#     node_metadata[node] = metadata

print(node_class_mapping)
