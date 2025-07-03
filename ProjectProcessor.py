from collections import defaultdict
import os
from MethodSizeReader import MethodSizeReader
from DotGraphAnalyzer import DotGraphAnalyzer
from MethodWriter import MethodWriter
class ProjectProcessor:
    def __init__(self, project_name, base_dir):
        self.project_name = project_name
        self.base_dir = base_dir
        self.size_file = os.path.join(base_dir, project_name, "method_parameters_sizeOf.csv")
        self.dot_dir = os.path.join(base_dir, project_name)
        self.output_file = os.path.join(base_dir, f"{project_name}_output_methods.txt")
        self.output_file_general_func_list = os.path.join(base_dir, f"{project_name}_output_general_functionality.txt")

    def process(self):
        # Step 1: Read size file
        reader = MethodSizeReader(self.size_file)
        method_size_map = reader.read()

        # Step 2: Set up writer
        writer = MethodWriter(self.output_file, self.output_file_general_func_list)

        feature_method_dict = defaultdict(list)
        
        # Step 3: Process each DOT file
        for file in os.listdir(self.dot_dir):
            if file.endswith(".dot"):
                dot_path = os.path.join(self.dot_dir, file)
                analyzer = DotGraphAnalyzer(dot_path, method_size_map)
                node_info = analyzer.get_node_info_considering_edges()
                
                featurename = file.split('_')[1].split('.')[0]  # Extracting the file name without extension
                methods = analyzer.get_class_method_names()
                feature_method_dict[featurename].extend(methods)

                writer.write_methods(node_info, methods, featurename)

        writer.write_general_functionality_list(feature_method_dict)

        # Step 4: Close writer
        #writer.close_file()