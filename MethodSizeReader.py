import csv

class MethodSizeReader:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.method_size_map = {}

    def read(self):
        with open(self.csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                full_signature = row['Method'].strip()
                total_size = int(row['Total Param Size'].strip())
                method_name = full_signature.split('(')[0]
                self.method_size_map[method_name] = total_size
        return self.method_size_map
