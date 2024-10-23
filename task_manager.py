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
    __task_file_delimiter = ","  # TODO: make sure delimiter is not present in the task description
    __max_task_id = None

    # TODO: task sate can only change back pending -> from deleted/completed

    def __init__(self):
        try:
            if (file_utils.is_file_present(self.__task_file_path)
                    and not file_utils.is_file_empty(self.__task_file_path)):
                # Get max_task_id
                last_line = file_utils.read_last_line(self.__task_file_path)
                self.__max_task_id = last_line.split(self.__task_file_delimiter)[0]
                try:
                    self.__max_task_id = int(self.__max_task_id)  # self.__max_task_id has to be a number
                except ValueError:
                    self.__max_task_id = 0
            else:
                # Create user.csv and task.csv if missing
                # task_update.csv will be recreated if task.csv is missing or empty
                file_utils.write(self.__task_file_path, 'w', Task.get_static_fields())
                file_utils.write(self.__task_update_file_path, 'w', Task.get_variable_fields())
                self.__max_task_id = 0
            print("#### Task manager is running. ####")
        except Exception as e:
            print(f"Task manager initialization failed: {e}")

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
            print("Please enter the task description:")
            task_desc = input()
            while not task_desc.strip():
                print("Task description can not be empty. Please re-enter:")
                task_desc = input()

            # TODO: task_desc can't be empty
            task = Task(self.__max_task_id + 1, user_name=user_name, desc=task_desc, created_at=file_utils.get_curr_time())
            # Save task's static details
            file_utils.write(self.__task_file_path, 'a', task.get_static_field_values())
            self.__max_task_id += 1
            print(f"Task #{self.__max_task_id} added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_tasks(self, user_name):
        try:
            tasks_to_show = []
            all_tasks = file_utils.get_static_values(self.__task_file_path, 'Task Owner', user_name)
            task_updates = file_utils.get_variable_values(self.__task_update_file_path)

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
            print("Please enter the task id:")
            task_id = input()
            while not task_id.strip():
                print("Task id can not be empty. Please re-enter:")
                task_id = input()

            # TODO: task_id can't be <1
            # TODO: terminal state can't be changed : use in-memory cache for this

            task = Task(task_id, state=new_state, updated_at=file_utils.get_curr_time())
            # Save task's variable details
            file_utils.write(self.__task_update_file_path, 'a', task.get_variable_field_values())
            if TaskManagerAction.COMPLETE_TASK == new_state:
                print(f"Task #{task_id} marked completed.")
            elif TaskManagerAction.DELETE_TASK == new_state:
                print(f"Task #{task_id} deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":

    task_manager = TaskManager()
    # Authenticate  the user
    username = "manishachopra8"

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
