import file_utils
from enum import Enum
from task import Task
from task import TaskState


class TaskManagerAction(Enum):
    ADD_TASK = 1
    LIST_TASKS = 2
    COMPLETE_TASK = 3
    DELETE_TASK = 4
    USER_LOGOUT = 5


class TaskManager:

    # This file would store the static task details like task_id, task_desc etc.
    __task_file_path = "./data/task.csv"
    # This file would store the variable task details like task_id, task_desc etc.
    __task_update_file_path = "./data/task_update.csv"
    # This file would store user details like username, password etc.
    __user_file_name = "user.csv"
    __task_delimiter = "|"
    __task_description_max_length = 255
    __max_task_id = None
    __task_update_cache = {}

    # TODO: task sate can only change back pending -> from deleted/completed

    def __init__(self):
        try:
            if (file_utils.is_file_present(self.__task_file_path)
                    and not file_utils.is_file_empty(self.__task_file_path)):
                # Get max_task_id
                last_line = file_utils.read_last_line(self.__task_file_path)
                self.__max_task_id = last_line.split(self.__task_delimiter)[0]
                try:
                    self.__max_task_id = int(self.__max_task_id)  # self.__max_task_id has to be a number
                except ValueError:
                    self.__max_task_id = 0

                    # task_update.csv will be recreated if task.csv has only headers
                    file_utils.write(self.__task_update_file_path, 'w',
                                     Task.get_variable_fields(), self.__task_delimiter)
            else:
                # Create user.csv and task.csv if missing
                # task_update.csv will be recreated if task.csv is missing or empty
                file_utils.write(self.__task_file_path, 'w', Task.get_static_fields(), self.__task_delimiter)
                file_utils.write(self.__task_update_file_path, 'w', Task.get_variable_fields(), self.__task_delimiter)
                self.__max_task_id = 0

            self.__load_cache()  # Load cache

            print("#### Task manager is running. ####")
        except Exception as e:
            print(f"Task manager initialization failed: {e}")

    def __load_cache(self):
        # Load task ids which have been updated
        self.__load_task_updates()

    def __load_task_updates(self):
        task_updates = file_utils.get_variable_values(self.__task_update_file_path, self.__task_delimiter)
        for task_id, task in task_updates.items():
            if TaskState.COMPLETED.name == task.state:
                self.__task_update_cache[int(task_id)] = True
            elif TaskState.DELETED.name == task.state:
                self.__task_update_cache[int(task_id)] = False

    @staticmethod
    def show_menu():
        print("\n\nPlease select any of the options below:\n"
              "\tEnter 1 to add a task\n"
              "\tEnter 2 to view tasks\n"
              "\tEnter 3 to mark a task as completed\n"
              "\tEnter 4 to delete a task\n"
              "\tEnter 5 to logout\n"
              )

    def add_task(self, user_name):
        try:
            # Task description can not
            #   1. be empty or
            #   2. have the __task_delimiter
            #   3. have more than 255 characters
            print("Please enter the task description:")
            while True:
                task_desc = input().strip()
                if not task_desc:
                    print("Task description can not be empty. Please re-enter: ")
                    continue
                if self.__task_delimiter in task_desc:
                    print(f"Task description can not have '{self.__task_delimiter} character'. Please re-enter: ")
                    continue
                if len(task_desc) > self.__task_description_max_length:
                    print(f"Task description must be less than {self.__task_description_max_length} characters. "
                          f"Please re-enter: ")
                    continue
                break

            task = Task(
                self.__max_task_id + 1,
                user_name=user_name,
                desc=task_desc,
                created_at=file_utils.get_curr_time()
            )
            # Save task's static details
            file_utils.write(self.__task_file_path, 'a', task.get_static_field_values(), self.__task_delimiter)
            self.__max_task_id += 1
            print(f"Task #{self.__max_task_id} added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_tasks(self, user_name):
        try:
            tasks_to_show = []
            all_tasks = file_utils.get_static_values(
                self.__task_file_path,
                self.__task_delimiter,
                'Task Owner',
                user_name
            )
            task_updates = file_utils.get_variable_values(self.__task_update_file_path, self.__task_delimiter)

            if not task_updates:
                tasks_to_show = all_tasks
            else:
                for task in all_tasks:
                    if task_updates.get(task.id) is not None:  # one task can only have one entry in task_update.csv
                        if TaskState.DELETED.name == task_updates[task.id].state:
                            continue
                        else:
                            task.state = task_updates[task.id].state
                            task.updated_at = task_updates[task.id].updated_at
                    tasks_to_show.append(task)

            # Pretty Print the tasks
            file_utils.pretty_print(tasks_to_show, Task.get_printable_fields())
        except Exception as e:
            print(f"An error occurred: {e.with_traceback()}")

    def update_task(self, new_state):
        try:
            #   1. Task id can not be empty
            #   2. Task id has to be an integer
            #   3. Task id can not be < 1
            #   4. Task id can not be greater than max task id currently in the system
            print("Please enter the task id: ")
            while True:
                task_id = input().strip()
                if not task_id:
                    print("Task id can not be empty. Please re-enter: ")
                    continue
                try:
                    task_id = int(task_id)  # task_id to be an integer
                except ValueError:
                    print("Task id has to be an integer. Please re-enter: ")
                    continue
                if task_id < 1:
                    print("Task id can not be less than 1. Please re-enter: ")
                    continue
                if task_id > int(self.__max_task_id):
                    print("Invalid task id. No such task is present. Please re-enter: ")
                    continue
                break
                
            # State of a task can't be changed if task is already in COMPLETED or DELETED state
            if task_id not in self.__task_update_cache:
                task = Task(task_id, state=new_state, updated_at=file_utils.get_curr_time())
                # Save task's variable details
                file_utils.write(self.__task_update_file_path, 'a',
                                 task.get_variable_field_values(), self.__task_delimiter)
                if TaskState.COMPLETED.name == new_state:
                    self.__task_update_cache[int(task_id)] = True
                    print(f"Task #{task_id} marked completed.")
                elif TaskState.DELETED.name == new_state:
                    self.__task_update_cache[int(task_id)] = False
                    print(f"Task #{task_id} deleted successfully.")
            else:
                task_bool_state = bool(self.__task_update_cache[task_id])
                task_state = TaskState.COMPLETED.name.lower() if task_bool_state else TaskState.DELETED.name.lower()
                print(f"Task #{task_id} has already been {task_state}.")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":

    task_manager = TaskManager()
    # Authenticate  the user
    username = "anuragsaxena"

    while True:
        TaskManager.show_menu()
        user_input = input("Your selection: ")

        if not isinstance(user_input, str):  # Input has to be a valid string
            print("The selection was invalid. Please enter an integer.")
            continue

        try:
            user_input = int(user_input)  # Input has to be an integer
        except ValueError:
            print("The selection was invalid. Please enter an integer.")
            continue

        user_input = int(user_input)  # Converting to integer as it is a valid number at this point

        if user_input == TaskManagerAction.ADD_TASK.value:
            task_manager.add_task(username)
        elif user_input == TaskManagerAction.LIST_TASKS.value:
            task_manager.list_tasks(username)
        elif user_input == TaskManagerAction.COMPLETE_TASK.value:
            task_manager.update_task(TaskState.COMPLETED.name)
        elif user_input == TaskManagerAction.DELETE_TASK.value:
            task_manager.update_task(TaskState.DELETED.name)
        elif user_input == TaskManagerAction.USER_LOGOUT.value:
            print("User logged out.")
            break
        else:
            print("Please choose a valid option.")  # Input has to be a valid selection
    print("GoodBye!")
