import os
import time
import csv
import sys

class WesterosArchive:
    def __init__(self):
        self.types = {}
        self.page_size = 10  # Maximum number of records per page

    def create_type(self, type_name, num_fields, primary_key_order, fields):
        if len(type_name) > 12:
            self.log_operation(f"create type {type_name} {num_fields} {primary_key_order} {' '.join(fields)}", 'failure')
            return
        if any(len(field.split()[0]) > 20 for field in fields):
            self.log_operation(f"create type {type_name} {num_fields} {primary_key_order} {' '.join(fields)}", 'failure')
            return
        if type_name in self.types:
            self.log_operation(f"create type {type_name} {num_fields} {primary_key_order} {' '.join(fields)}", 'failure')
            return
        self.types[type_name] = {
            "num_fields": num_fields,
            "primary_key_order": primary_key_order,
            "fields": fields
        }
        with open(f'{type_name}.csv', 'w', newline='') as type_file:
            writer = csv.writer(type_file)
            writer.writerow(fields)  # Header for fields
        self.log_operation(f"create type {type_name} {num_fields} {primary_key_order} {' '.join(fields)}", 'success')
        print(f"Type created: {type_name}")

    def create_record(self, type_name, values):
        if type_name not in self.types:
            self.log_operation(f"create record {type_name} {' '.join(values)}", 'failure')
            return
        primary_key_index = self.types[type_name]['primary_key_order']
        primary_key = values[primary_key_index]
        records = self.read_records(type_name)
        for record in records:
            if record[primary_key_index] == primary_key:
                self.log_operation(f"create record {type_name} {' '.join(values)}", 'failure')
                return
        records.append(values)
        self.write_records(type_name, records)
        self.log_operation(f"create record {type_name} {' '.join(values)}", 'success')
        print(f"Record created in {type_name}: {values}")

    def delete_record(self, type_name, primary_key):
        if type_name not in self.types:
            self.log_operation(f"delete record {type_name} {primary_key}", 'failure')
            return
        primary_key_index = self.types[type_name]['primary_key_order']
        records = self.read_records(type_name)
        for record in records:
            if record[primary_key_index] == primary_key:
                records.remove(record)
                self.write_records(type_name, records)
                self.log_operation(f"delete record {type_name} {primary_key}", 'success')
                print(f"Record deleted from {type_name} with primary key: {primary_key}")
                return
        self.log_operation(f"delete record {type_name} {primary_key}", 'failure')

    def search_record(self, type_name, primary_key):
        if type_name not in self.types:
            self.log_operation(f"search record {type_name} {primary_key}", 'failure')
            return None
        primary_key_index = self.types[type_name]['primary_key_order']
        try:
            with open(f'{type_name}.csv', 'r', newline='') as type_file:
                reader = csv.reader(type_file)
                next(reader)  # Skip header
                page = []
                for row in reader:
                    if row[0].startswith('PAGE_HEADER'):
                        continue
                    page.append(row)
                    if len(page) == self.page_size:
                        for record in page:
                            if record[primary_key_index] == primary_key:
                                self.log_operation(f"search record {type_name} {primary_key}", 'success')
                                print(f"Record found in {type_name} with primary key: {primary_key}")
                                return record
                        page = []
                for record in page:
                    if record[primary_key_index] == primary_key:
                        self.log_operation(f"search record {type_name} {primary_key}", 'success')
                        print(f"Record found in {type_name} with primary key: {primary_key}")
                        return record
        except FileNotFoundError:
            self.log_operation(f"search record {type_name} {primary_key}", 'failure')
            print(f"File for type {type_name} not found.")
            return None

        self.log_operation(f"search record {type_name} {primary_key}", 'failure')
        print(f"Record not found in {type_name} with primary key: {primary_key}")
        return None

    def log_operation(self, operation, status):
        with open('log.txt', mode='a', newline='') as log_file:
            log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            log_writer.writerow([int(time.time()), operation, status])
        print(f"Logged operation: {operation} with status: {status}")

    def read_records(self, type_name):
        records = []
        try:
            with open(f'{type_name}.csv', 'r', newline='') as type_file:
                reader = csv.reader(type_file)
                next(reader)  # Skip header
                for row in reader:
                    if not row[0].startswith('PAGE_HEADER'):
                        records.append(row)
        except FileNotFoundError:
            pass  # File will be created when the first record is added
        return records

    def write_records(self, type_name, records):
        page_count = 1
        with open(f'{type_name}.csv', 'w', newline='') as type_file:
            writer = csv.writer(type_file)
            writer.writerow(self.types[type_name]['fields'])
            current_page_records = []
            for record in records:
                current_page_records.append(record)
                if len(current_page_records) == self.page_size:
                    writer.writerow([f'PAGE_HEADER {page_count} {len(current_page_records)}'])
                    writer.writerows(current_page_records)
                    current_page_records = []
                    page_count += 1
            if current_page_records:
                writer.writerow([f'PAGE_HEADER {page_count} {len(current_page_records)}'])
                writer.writerows(current_page_records)

def main(input_file_path='input.txt'):
    archive = WesterosArchive()
    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            parts = line.strip().split()
            operation = parts[0]
            if operation == 'create' and parts[1] == 'type':
                type_name = parts[2]
                num_fields = int(parts[3])
                primary_key_order = int(parts[4]) - 1  # Convert to zero-based index
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
