# Westeros Archive

The Westeros Archive is a Python-based application designed to manage types and records in a CSV format. It supports creating new types, adding records, deleting records, and searching for records. This project is implemented with the goal of managing large datasets efficiently by utilizing pagination.


## Running the Program

1. Navigate to the project directory:

`cd <project_directory>`

2. Ensure your input commands are in a file named `input.txt` in the same directory as the script.
3. Run the program:

`python3 archive.py [input_file_path]`

If no input file path is provided, it defaults to `input.txt`.

## Features

1. **Create Type**: Define a new type with a specified number of fields and a primary key.
2. **Create Record**: Add a new record to an existing type.
3. **Delete Record**: Remove a record based on the primary key.
4. **Search Record**: Find a record by its primary key.
5. **Logging**: Log all operations with timestamps and their success or failure status.

## Usage

### Input Format

The input commands should be provided in a file named `input.txt`. Each line in the file should follow the specified format:

- **Create Type**: `create type <type_name> <num_fields> <primary_key_order> <field1> <field2> ...`
- **Create Record**: `create record <type_name> <value1> <value2> ...`
- **Delete Record**: `delete record <type_name> <primary_key>`
- **Search Record**: `search record <type_name> <primary_key>`

### Example

- create type Person 3 1 Name Age City
- create record Person John 30 Winterfell
- create record Person Arya 18 Winterfell
- delete record Person Arya
- search record Person John


## Class Structure

### `WesterosArchive`

This class is responsible for managing types and records, including creating, deleting, searching records, and logging operations.

#### Attributes

- `types`: Dictionary to store type definitions.
- `page_size`: Maximum number of records per page.
- `max_pages_per_file`: Maximum number of pages per file.
- `max_type_length`: Maximum length of type names.
- `max_field_length`: Maximum length of field names.
- `max_fields`: Maximum number of fields a type can have.

#### Methods

- `create_type()`: Creates a new type.
- `create_record()`: Adds a new record to a type.
- `delete_record()`: Deletes a record from a type.
- `search_record()`: Searches for a record in a type.
- `log_operation()`: Logs the operations.
- `read_records()`: Reads records from the file.
- `write_records()`: Writes records to the file.

## Functions

### `main(input_file_path='input.txt')`

- Reads commands from the input file.
- Processes each command by calling the appropriate methods in the `WesterosArchive` class.


## Logging

All operations are logged in a file named `log.txt` with the following format:

`[timestamp], [operation], [status]`


The log file helps in tracking the success or failure of each operation along with the time of execution.

