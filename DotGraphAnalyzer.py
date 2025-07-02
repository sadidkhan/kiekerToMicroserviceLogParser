import re
from collections import defaultdict, deque

class DotGraphAnalyzer:
    def __init__(self, dot_filepath, method_size_map):
        self.dot_filepath = dot_filepath
        self.method_size_map = method_size_map
        self.dot_data = self._load_dot_file()
        self.adjacency_list = self._create_adjacency_list()
        self.node_class_mapping = self._create_depNode_method_mapping()
        self.node_depth = self._calculate_node_depth()
        self.node_method_depth_mapping_considering_edges = self.merge_nodes_considering_edges()
        self.node_method_depth_mapping = self.merge_nodes()

    def _load_dot_file(self):
        with open(self.dot_filepath, 'r') as f:
            return f.read()

    def _create_adjacency_list(self):
        edges = re.findall(r'(depNode_\d+)\s*->\s*(depNode_\d+)', self.dot_data)
        adjacency_list = defaultdict(list)
        for source, target in edges:
            adjacency_list[source].append(target)
        return adjacency_list

    def _extract_metadata(self, node):
        label = node['label']
        label_clean = label.replace("\\n", "").strip()

        label_clean = self.extract_method_name_from_label(node, label_clean)

        for part in label_clean.split(','):
            if ':' in part:
                key, value = part.split(':', 1)
                node[key.strip()] = value.strip()

    def extract_method_name_from_label(self, node, label_clean):
        if 'Entry' in label_clean:
            node['methodname'] = 'Entry'
            return label_clean.replace('Entry', '').strip()
        
        method_match = re.match(r'(?:<([^>]+)>|(\w+\(\.*\)))', label_clean)
        if method_match:
            raw_methodname = method_match.group(1) if method_match.group(1) else method_match.group(2)
            node['methodname'] = raw_methodname.replace('()', '').replace('(..)', '')
            label_clean = label_clean[method_match.end():].replace('()', '').replace('(..)', '').strip()
        return label_clean

    def get_sizeof_method(self, node_info):
        method_name = node_info.get('methodname', '')
        size = 0
        if method_name in self.method_size_map:
            size = self.method_size_map[method_name]
            
        node_info['size'] = size
        
        
        
    def _create_depNode_method_mapping(self):
        node_class_mapping = {}
        #{"depNode_0": {"label": "Entry", "class": "root"}}
        current_class = None

        for line in self.dot_data.splitlines():
            class_match = re.search(r'label\s*=\s*"<<assembly component>>\\n@[\d]+:(.*?)"', line)
            if class_match:
                current_class = class_match.group(1).strip()

            node_match = re.match(r'"(depNode_\d+)"\s+\[label="([^"]+)"', line)
            if node_match:
                node_id, label = node_match.groups()
                if current_class is None and 'Entry' in label:
                    current_class = "root"
                    
                label_clean = label.replace("\\n", " ").replace("\n", " ").strip()
                node_class_mapping[node_id] = {
                    "label": label_clean,
                    "class": current_class
                }
                self._extract_metadata(node_class_mapping[node_id])
                self.get_sizeof_method(node_class_mapping[node_id])
        
        return node_class_mapping

    def _calculate_node_depth(self):
        depth = {}

        for node in self.adjacency_list:
            if node not in depth:
                depth[node] = 0
                # self.node_class_mapping[node]['depth'] = 0
                queue = deque([node])

                while queue:
                    current = queue.popleft()
                    current_depth = depth[current]

                    for neighbor in self.adjacency_list.get(current, []):
                        if neighbor not in depth:
                            depth[neighbor] = current_depth + 1
                            # self.node_class_mapping[neighbor]['depth'] = depth[neighbor]
                            queue.append(neighbor)
        
        return depth

    def get_node_info(self):
        return self.node_method_depth_mapping
    
    def get_node_info_considering_edges(self):
        return self.node_method_depth_mapping_considering_edges
    
    def merge_nodes_considering_edges(self):
        node_method_depth_mapping = {}
        for node_id, node_info in self.node_depth.items():
            if node_id in self.node_class_mapping:
                node_method_depth_mapping[node_id] = self.node_class_mapping[node_id]
                node_method_depth_mapping[node_id]['depth'] = node_info

        return node_method_depth_mapping
    
    def merge_nodes(self):
        node_method_depth_mapping = {}
        for node_id, node_info in self.node_class_mapping.items():
            if node_id in self.node_class_mapping:
                node_method_depth_mapping[node_id] = node_info
                node_method_depth_mapping[node_id]['depth'] = self.node_depth[node_id]

        return node_method_depth_mapping

    
    def get_class_method_names(self):
        return sorted([
            f"{data['class']}.{data['methodname']}" for data in self.node_class_mapping.values() if 'methodname' in data and 'class' in data
        ])
