import os
import time
import csv
import sys

class WesterosArchive:
    def __init__(self):
        self.types = {}

    def create_type(self, type_name, num_fields, primary_key_order, fields):
        if type_name in self.types:
            self.log_operation(f"create type {type_name} {num_fields} {primary_key_order} {' '.join(fields)}", 'failure')
            return
        self.types[type_name] = {
            "num_fields": num_fields,
            "primary_key_order": primary_key_order,
            "fields": fields,
            "records": []
        }
        self.log_operation(f"create type {type_name} {num_fields} {primary_key_order} {' '.join(fields)}", 'success')

    def create_record(self, type_name, values):
        if type_name not in self.types:
            self.log_operation(f"create record {type_name} {' '.join(values)}", 'failure')
            return
        primary_key = values[self.types[type_name]['primary_key_order']]
        for record in self.types[type_name]['records']:
            if record[self.types[type_name]['primary_key_order']] == primary_key:
                self.log_operation(f"create record {type_name} {' '.join(values)}", 'failure')
                return
        self.types[type_name]['records'].append(values)
        self.log_operation(f"create record {type_name} {' '.join(values)}", 'success')

    def delete_record(self, type_name, primary_key):
        if type_name not in self.types:
            self.log_operation(f"delete record {type_name} {primary_key}", 'failure')
            return
        for record in self.types[type_name]['records']:
            if record[self.types[type_name]['primary_key_order']] == primary_key:
                self.types[type_name]['records'].remove(record)
                self.log_operation(f"delete record {type_name} {primary_key}", 'success')
                return
        self.log_operation(f"delete record {type_name} {primary_key}", 'failure')

    def search_record(self, type_name, primary_key):
        if type_name not in self.types:
            self.log_operation(f"search record {type_name} {primary_key}", 'failure')
            return None
        for record in self.types[type_name]['records']:
            if record[self.types[type_name]['primary_key_order']] == primary_key:
                self.log_operation(f"search record {type_name} {primary_key}", 'success')
                return record
        self.log_operation(f"search record {type_name} {primary_key}", 'failure')
        return None

    def log_operation(self, operation, status):
        with open('log.csv', mode='a', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow([int(time.time()), operation, status])

def main(input_file_path='input.txt'):
    archive = WesterosArchive()
    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            parts = line.strip().split()
            operation = parts[0]
            if operation == 'create' and parts[1] == 'type':
                type_name = parts[2]
                num_fields = int(parts[3])
                primary_key_order = int(parts[4])
                fields = parts[5:]
                archive.create_type(type_name, num_fields, primary_key_order, fields)
            elif operation == 'create' and parts[1] == 'record':
                type_name = parts[2]
                values = parts[3:]
                archive.create_record(type_name, values)
            elif operation == 'delete' and parts[1] == 'record':
                type_name = parts[2]
                primary_key = parts[3]
                archive.delete_record(type_name, primary_key)
            elif operation == 'search' and parts[1] == 'record':
                type_name = parts[2]
                primary_key = parts[3]
                record = archive.search_record(type_name, primary_key)
                if record:
                    with open('output.txt', 'a') as output_file:
                        output_file.write(' '.join(record) + '\n')
                else:
                    with open('output.txt', 'a') as output_file:
                        output_file.write('Record not found\n')

if __name__ == '__main__':
    input_file_path = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file_path)
    