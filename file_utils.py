import os
from time import gmtime, strftime
from prettytable import PrettyTable
from csv import writer
from csv import DictReader


def write(file_name, mode, data):
    with open(file_name, mode) as file:

        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(file)
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(data)


def pretty_print(file_name, user_name):

    # Create a PrettyTable object
    table = PrettyTable()

    columns_to_include = ['Task Id', 'Task Description', 'Task State', 'Created At', 'Updated At']

    with open(file_name, newline='') as file:
        file_reader = DictReader(file)
        headers = [header for header in file_reader.fieldnames if header in columns_to_include]
        table.field_names = headers

        for row in file_reader:
            if row['Task Owner'] == user_name:
                table.add_row([row[column] for column in headers])

    if not table.rows:
        print("No tasks are present. Table is Empty.")
    print(table)


def read_last_line(file_name):
    with open(file_name, 'rb') as file:
        file.seek(-1, 2)  # Jump to the last byte.
        if file.read(1) == b'\n':  # If the file ends with a newline, step back one more byte.
            file.seek(-2, 1)
        while file.read(1) != b'\n':  # Until EOL is found.
            if file.tell() == 1:  # If we're at the start of the file.
                file.seek(0)
                break
            file.seek(-2, 1)  # Step back one byte.
        last_line = file.readline().decode()
        file.close()
        return last_line


def get_curr_time():
    return strftime("%Y-%m-%d %H:%M:%S GMT", gmtime())


def is_file_present(file_path):
    return os.path.exists(file_path)


def is_file_empty(file_path):
    return os.stat(file_path).st_size == 0
