import re
from collections import defaultdict
from collections import deque


def create_adjacency_list(dot_data):
    # Create an adjacency list from the DOT data
    edges = re.findall(r'(depNode_\d+)\s*->\s*(depNode_\d+)', dot_data)

    adjacency_list = defaultdict(list)

    for edge in edges:  
        source, target = edge
        adjacency_list[source].append(target)
    
    return adjacency_list


def extract_metadata(node):
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
            
            
def create_depNode_method_mapping():
    node_class_mapping = {"depNode_0": {"label": "Entry", "class": "root"}}
    current_class = None

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
            extract_metadata(node_class_mapping[node_id])
    
    return node_class_mapping
    

def calculate_node_depth():
    depth = {}

    # Loop through all nodes (handles disconnected graphs)
    for node in adjacency_list:
        if node not in depth:
            depth[node] = 0
            node_class_mapping[node]['depth'] = depth[node]
        
        # Start BFS from this node
            queue = deque([node])

            while queue:
                current = queue.popleft()
                current_depth = depth[current]

                for neighbor in adjacency_list.get(current, []):
                    if neighbor not in depth:
                        depth[neighbor] = current_depth + 1
                        node_class_mapping[neighbor]['depth'] = depth[neighbor]
                        queue.append(neighbor)   


# Load the DOT file content
with open("./data/JpetStore/assemblyOperationDependencyGraph_category.dot") as f:
    dot_data = f.read()
    

node_class_mapping = create_depNode_method_mapping()
adjacency_list = create_adjacency_list(dot_data)
calculate_node_depth()
print(node_class_mapping)






                

    
