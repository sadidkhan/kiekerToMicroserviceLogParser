class MethodWriter:
    def __init__(self, output_path):
        self.output_path = output_path

    def write_methods(self, node_class_mapping, method_names, featurename):
        with open(self.output_path, "a", encoding="utf-8") as file:
            
            file.write(f'SF:{featurename}<')
            file.write(','.join(method_names) + ' ')
            file.write('>')
            
            for node, info in node_class_mapping.items():
                class_name = info.get("class")
                method_name = info.get("methodname")
                depth = info.get("depth", 0)
                size = info.get("total", 0)
                thread = "main"

                if class_name and method_name:
                    line = f"Class:{class_name}#Method:{method_name}#SizeOf:{size}#Deep:{depth}#Thread:{thread}\n"
                    file.write(line)
