import os
from time import gmtime, strftime
from prettytable import PrettyTable
from csv import DictReader, writer
from task import Task, TaskState

'''
Writes data to a csv file 
Parameters:
file_name (str): The path to the file
mode (str): 'w' for writing and 'a' for appending the data
data (list): list of values to be written
delimiter (str): delimiter between the values
'''


def write(file_name, mode, data, delimiter):
    with open(file_name, mode) as file:
        file_writer = writer(file, delimiter=delimiter)
        file_writer.writerow(data)


'''
Reads static values of task i.e.['Task Id', 'Task Owner', 'Task Description', 'Created At']
and filters the data on filter_header
Parameters:
file_name (str): The path to the file
delimiter (str): delimiter between the values
static_field_headers (list): Headers for static fields of Task. 
filter_header (str): Header of the field to filter
filter_value (str): value of the field to filter

Returns:
list: The filtered list of task for a user
'''


def get_static_values(file_name, delimiter, static_field_headers, filter_header, filter_value):
    tasks = []
    with open(file_name, 'r', newline='') as file:
        file_reader = DictReader(file, delimiter=delimiter)
        for row in file_reader:
            if filter_header is not None and filter_value is not None and row[static_field_headers[1]] == filter_value:
                task = Task(row[static_field_headers[0]],
                            user_name=row[static_field_headers[1]],
                            desc=row[static_field_headers[2]],
                            state=TaskState.PENDING.name,
                            created_at=row[static_field_headers[3]],
                            updated_at=row[static_field_headers[3]])  # updated_at is same as created_at when object is created
                tasks.append(task)
    return tasks


'''
Reads dynamic values of task i.e.['Task Id', 'Task State', 'Updated At']
Parameters:
file_name (str): The path to the file
delimiter (str): delimiter between the values
variable_field_headers (list): Headers for static fields of Task. 

Returns:
dict: dictionary of {id: task}
'''


def get_variable_values(file_name, delimiter, variable_field_headers):
    task_updates = {}
    with open(file_name, 'r', newline='') as file:
        file_reader = DictReader(file, delimiter=delimiter)
        for row in file_reader:
            task = Task(row[variable_field_headers[0]],
                        state=row[variable_field_headers[1]],
                        updated_at=row[variable_field_headers[2]])
            task_updates[row[variable_field_headers[0]]] = task
    return task_updates


'''
Prints the tasks along with the headers
Parameters:
tasks (list): The list of tasks
headers (list): list of headers
'''


def pretty_print(tasks, headers):

    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = headers

    for task in tasks:
        table.add_row([task.id, task.desc, task.state, task.created_at, task.updated_at])

    print(table)


'''
Reads last line of the file
Parameters:
file_name (str): The path to the file

Returns:
str: last line of the file
'''


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


'''
Checks if a value is unique in a file for a header
Parameters:
filename (str): The path to the file
delimiter (str): delimiter between the values
value_to_find (str): value to find in a header
value_header (str): header in which value is to be found
 
Returns:
bool: True if value is unique  else False
'''


def is_value_unique(filename, delimiter, value_to_find, value_header):
    with open(filename, 'r') as file:
        reader = DictReader(file, delimiter=delimiter)
        for row in reader:
            if row[value_header] == value_to_find:
                return False
    return True


'''
Matches values ina given file
Parameters:
filename (str): The path to the file
delimiter (str): delimiter between the values
values_to_match (list): values to match in a corresponding header
value_headers (list): corresponding headers for which value is to be matched
 
Returns:
bool: True if value is matched else False
'''


def match_values(filename, delimiter, values_to_match, value_headers):
    value_match = [False, False]
    with open(filename, 'r') as file:
        reader = DictReader(file, delimiter=delimiter)
        for row in reader:
            value_match = [False, False]
            if row[value_headers[0]] == values_to_match[0]:
                value_match[0] = True
                if row[value_headers[1]] == values_to_match[1]:
                    value_match[1] = True
                break
        return value_match


'''
Gets current GMT time in 'YYYY-MM-DD HH:MM:SS GMT' format

Returns:
str: current GMT time in 'YYYY-MM-DD HH:MM:SS GMT' format
'''


def get_curr_time():
    return strftime("%Y-%m-%d %H:%M:%S GMT", gmtime())


'''
Checks if a file is present in file system

Returns:
bool: True if a file is present in file system else False
'''
def is_file_present(file_path):
    return os.path.exists(file_path)


'''
Checks if a file is empty

Returns:
bool: True if a file is empty else False
'''
def is_file_empty(file_path):
    return os.stat(file_path).st_size == 0
