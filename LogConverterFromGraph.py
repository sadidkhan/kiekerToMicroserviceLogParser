from DotGraphAnalyzer import DotGraphAnalyzer
from MethodSizeReader import MethodSizeReader
from MethodWriter import MethodWriter

reader = MethodSizeReader('./data/JpetStore/method_parameters_sizeOf.csv')
method_size_map = reader.read()

analyzer = DotGraphAnalyzer('./data/JpetStore/assemblyOperationDependencyGraph_category.dot', method_size_map)
node_info = analyzer.get_node_info()

for i, (node, info) in enumerate(node_info.items(), start=1):
    print(f"{i}. | Class: {info.get('class')} | Method: {info.get('methodname')} | Depth: {info.get('depth')}")


node_info = analyzer.get_node_info_considering_edges()

for i, (node, info) in enumerate(node_info.items(), start=1):
    print(f"{i}. | Class: {info.get('class')} | Method: {info.get('methodname')} | Depth: {info.get('depth')}")

methods = analyzer.get_class_method_names()

writer = MethodWriter('output_methods.txt')
writer.write_methods(node_info, methods)

