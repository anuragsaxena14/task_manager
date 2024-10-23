import os
from time import gmtime, strftime
from csv import writer


def write(file_name, mode, data):
    with open(file_name, mode) as file:

        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(file)
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(data)

        # Close the file object
        file.close()


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
