class MethodWriter:
    def __init__(self, output_path, output_file_general_func_list):
        self.output_path = output_path
        self.output_path_general_func_list = output_file_general_func_list

    def write_methods(self, node_class_mapping, method_names, featurename):
        with open(self.output_path, "a", encoding="utf-8") as file:
            
            file.write(f'SF:{featurename}<')
            file.write(','.join(method_names) + '>\n')
            
            for node, info in node_class_mapping.items():
                class_name = info.get("class")
                method_name = info.get("methodname")
                depth = info.get("depth", 0)
                size = info.get("total", 0)
                thread = "main"

                if class_name and method_name:
                    line = f"Class:{class_name}#Method:{method_name}#SizeOf:{size}#Deep:{depth}#Thread:{thread}\n"
                    file.write(line)
                    
                    
    def write_general_functionality_list(self, feature_method_dict):
        with open(self.output_path_general_func_list, "a", encoding="utf-8") as file:
            # Write SF: only once at the beginning
            file.write('SF:')
            
            # Loop through the dictionary and write each feature and its methods
            for featurename, method_names in feature_method_dict.items():
                file.write(f'{featurename}<')
                file.write(','.join(method_names))
                file.write('>#')  # Add a separator for each feature
            
            # Remove the trailing '#' and add a newline
            file.truncate(file.tell() - 1)  # Remove the trailing '#'
            file.write('\n')
