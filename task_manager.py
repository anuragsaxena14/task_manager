import file_utils
from enum import Enum
from task import Task


class TaskManagerAction(Enum):
    ADD_TASK = 1
    VIEW_TASK = 2
    COMPLETE_TASK = 3
    DELETE_TASK = 4
    USER_LOGOUT = 5


class TaskManager:
    # This file would store the task details like task_id, task_desc etc.
    __data_path = "./data/"
    __task_file_name = "task.csv"
    # This file would store user details like username, password etc.
    __user_file_name = "user.csv"
    __task_file_delimiter = ","
    __max_task_id = None

    def __init__(self):
        try:
            if (file_utils.is_file_present(self.__data_path + self.__task_file_name)
                    and not file_utils.is_file_empty(self.__data_path + self.__task_file_name)):
                # Get max_task_id
                last_line = file_utils.read_last_line(self.__data_path + self.__task_file_name)
                self.__max_task_id = last_line.split(self.__task_file_delimiter)[0]
                if self.__max_task_id is not type(int):
                    # File is empty and header data is read, so reset the max_task_id
                    self.__max_task_id = 0
                print(f"max_task_id: {self.__max_task_id}")
            else:
                # Create user.csv and task.csv if missing
                file_utils.write(self.__data_path + self.__task_file_name, 'w', Task.get_fields())
                self.__max_task_id = 0
            print("Task manager running.")
        except Exception as e:
            print(f"Task manager initialization failed: {e}")

    @staticmethod
    def show_menu():
        print("Please select any of the options below:\n"
              "\tEnter 1 to add a task\n"
              "\tEnter 2 to view tasks\n"
              "\tEnter 3 to mark a task as completed\n"
              "\tEnter 4 to delete a task\n"
              "\tEnter 5 to logout\n"
              )

    def add_task(self, user_name):
        try:
            print("Please enter the task description:")
            task_desc = input()
            task = Task(self.__max_task_id + 1, user_name, task_desc)
            # save task
            file_utils.write(self.__data_path + self.__task_file_name, 'a', task.get_values())
            self.__max_task_id += 1
            print(f"Task #{self.__max_task_id} added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":

    task_manager = TaskManager()
    # Authenticate  the user
    username = "anuragsaxena14"

    while True:
        TaskManager.show_menu()
        user_input = input("Your selection: ")

        if not isinstance(user_input, str):  # Input has to be a valid string
            print("The selection was invalid. Please enter a number.")
            continue

        try:
            user_input = int(user_input)  # Input has to be a number
        except ValueError:
            print("The selection was invalid. Please enter a number.")
            continue

        user_input = int(user_input)  # Converting to integer as it is a valid number at this point

        if user_input == TaskManagerAction.ADD_TASK.value:
            task_manager.add_task(username)
        elif user_input == TaskManagerAction.VIEW_TASK.value:
            print("Viewing a task")
        elif user_input == TaskManagerAction.COMPLETE_TASK.value:
            print("Completing a task")
        elif user_input == TaskManagerAction.DELETE_TASK.value:
            print("Deleting a task")
        elif user_input == TaskManagerAction.USER_LOGOUT.value:
            print("User logged out")
            break
        else:
            print("Please choose a valid option.")  # Input has to be a valid selection
    print("GoodBye!")
