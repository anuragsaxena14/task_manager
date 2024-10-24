import os
from time import gmtime, strftime
from prettytable import PrettyTable
from csv import DictReader, writer
from task import Task, TaskState


def write(file_name, mode, data, delimiter):
    with open(file_name, mode) as file:
        file_writer = writer(file, delimiter=delimiter)
        file_writer.writerow(data)


def get_static_values(file_name, delimiter, filter_header=None, filter_value=None):
    tasks = []
    static_fields = Task.get_static_fields()
    with open(file_name, 'r', newline='') as file:
        file_reader = DictReader(file, delimiter=delimiter)
        for row in file_reader:
            if filter_header is not None and filter_value is not None and row[static_fields[1]] == filter_value:
                task = Task(row[static_fields[0]],
                            user_name=row[static_fields[1]],
                            desc=row[static_fields[2]],
                            state=TaskState.PENDING.name,
                            created_at=row[static_fields[3]],
                            updated_at=row[static_fields[3]])  # updated_at is same as created_at when object is created
                tasks.append(task)
    return tasks


def get_variable_values(file_name, delimiter):
    task_updates = {}
    variable_fields = Task.get_variable_fields()
    with open(file_name, 'r', newline='') as file:
        file_reader = DictReader(file, delimiter=delimiter)
        for row in file_reader:
            task = Task(row[variable_fields[0]],
                        state=row[variable_fields[1]],
                        updated_at=row[variable_fields[2]])
            task_updates[row[variable_fields[0]]] = task
    return task_updates


def pretty_print(tasks, headers):

    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = headers

    for task in tasks:
        table.add_row([task.id, task.desc, task.state, task.created_at, task.updated_at])

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
