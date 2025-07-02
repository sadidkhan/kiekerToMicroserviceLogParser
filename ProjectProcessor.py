import os

class ProjectProcessor:
    def __init__(self, project_name, base_dir):
        self.project_name = project_name
        self.base_dir = base_dir
        self.size_file = os.path.join(base_dir, project_name, "method_parameters_sizeOf.csv")
        self.dot_dir = os.path.join(base_dir, project_name)
        self.output_file = os.path.join(base_dir, f"{project_name}_output_methods.txt")

    def process(self):
        from MethodSizeReader import MethodSizeReader
        from DotGraphAnalyzer import DotGraphAnalyzer
        from MethodWriter import MethodWriter

        # Step 1: Read size file
        reader = MethodSizeReader(self.size_file)
        method_size_map = reader.read()

        # Step 2: Set up writer
        writer = MethodWriter(self.output_file)
        #writer.open_file()  # Explicit open

        # Step 3: Process each DOT file
        for file in os.listdir(self.dot_dir):
            if file.endswith(".dot"):
                dot_path = os.path.join(self.dot_dir, file)
                analyzer = DotGraphAnalyzer(dot_path, method_size_map)
                node_info = analyzer.get_node_info_considering_edges()
                methods = analyzer.get_class_method_names()
                
                featurename = file.split('_')[1]  # Extracting the file name without extension
                writer.write_methods(node_info, methods, featurename)

        # Step 4: Close writer
        #writer.close_file()