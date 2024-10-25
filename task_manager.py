import utils
from enum import Enum
from task import Task
from task import TaskState


class TaskManagerAction(Enum):
    ADD_TASK = 1
    LIST_TASKS = 2
    COMPLETE_TASK = 3
    DELETE_TASK = 4
    EXIT = 5


class TaskManager:

    # This file would store the static task details like task_id, task_desc etc.
    __task_file_path = "./task.csv"
    # This file would store the variable task details like task_id, task_desc etc.
    __task_update_file_path = "./task_update.csv"
    __task_delimiter = "|"
    __task_description_max_length = 255
    __max_task_id = None
    __task_update_cache = {}

    # ['Task Id', 'Task Owner', 'Task Description', 'Created At']
    __task_static_field_list = [Task.field_to_header_mapping()[0][1], Task.field_to_header_mapping()[1][1],
                                Task.field_to_header_mapping()[2][1], Task.field_to_header_mapping()[4][1]]

    # ['Task Id', 'Task State', 'Updated At']
    __task_variable_field_list = [Task.field_to_header_mapping()[0][1], Task.field_to_header_mapping()[3][1],
                                  Task.field_to_header_mapping()[5][1]]

    # ['Task Id', 'Task Description', 'Task State', 'Created At', 'Updated At']
    __task_display_field_list = [Task.field_to_header_mapping()[0][1], Task.field_to_header_mapping()[2][1],
                                 Task.field_to_header_mapping()[3][1], Task.field_to_header_mapping()[4][1],
                                 Task.field_to_header_mapping()[5][1]]

    def __init__(self):
        try:
            if (utils.is_file_present(self.__task_file_path)
                    and not utils.is_file_empty(self.__task_file_path)):
                # Get max_task_id
                last_line = utils.read_last_line(self.__task_file_path)
                self.__max_task_id = last_line.split(self.__task_delimiter)[0]
                try:
                    self.__max_task_id = int(self.__max_task_id)  # self.__max_task_id has to be a number
                except ValueError:
                    self.__max_task_id = 0

                    # task_update.csv will be recreated if task.csv has only headers
                    utils.write(self.__task_update_file_path, 'w',
                                     self.__task_variable_field_list, self.__task_delimiter)
            else:
                # Create task.csv if missing
                # task_update.csv will also be recreated if task.csv is missing or empty
                utils.write(self.__task_file_path, 'w', self.__task_static_field_list, self.__task_delimiter)
                utils.write(self.__task_update_file_path, 'w', self.__task_variable_field_list, self.__task_delimiter)
                self.__max_task_id = 0

            self.__load_cache()  # Load cache
        except Exception as e:
            print(f"\nTask manager initialization failed: {e}")

    def __load_cache(self):
        # Load task ids which have been updated
        self.__load_task_updates()

    def __load_task_updates(self):
        task_updates = utils.get_variable_values(self.__task_update_file_path, self.__task_delimiter,
                                                      self.__task_variable_field_list)
        for task_id, task in task_updates.items():
            if TaskState.COMPLETED.name == task.state:
                self.__task_update_cache[int(task_id)] = True
            elif TaskState.DELETED.name == task.state:
                self.__task_update_cache[int(task_id)] = False

    def __add_task(self, user_name):
        try:
            # Task description can not
            #   1. be empty or
            #   2. have the __task_delimiter
            #   3. have more than 255 characters
            print("\nPlease enter the task description:")
            while True:
                task_desc = input().strip()
                if not task_desc:
                    print("\nTask description can not be empty. Please re-enter: ")
                    continue
                if self.__task_delimiter in task_desc:
                    print(f"\nTask description can not have '{self.__task_delimiter} character'. Please re-enter: ")
                    continue
                if len(task_desc) > self.__task_description_max_length:
                    print(f"\nTask description must be less than {self.__task_description_max_length} characters. "
                          f"Please re-enter: ")
                    continue
                break

            # Save task's static details
            utils.write(self.__task_file_path, 'a',
                        [self.__max_task_id + 1, user_name, task_desc,  utils.get_curr_time()], self.__task_delimiter)
            self.__max_task_id += 1
            print(f"\nTask #{self.__max_task_id} added successfully.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

    def __list_tasks(self, user_name):
        try:
            tasks_to_show = []
            all_tasks = utils.get_static_values(
                self.__task_file_path,
                self.__task_delimiter,
                self.__task_static_field_list,
                self.__task_static_field_list[1],
                user_name
            )
            task_updates = utils.get_variable_values(self.__task_update_file_path, self.__task_delimiter,
                                                     self.__task_variable_field_list)
            if not task_updates:
                tasks_to_show = all_tasks
            else:
                for task in all_tasks:
                    if task_updates.get(task.id) is not None:  # one task can only have one entry in task_updates
                        if TaskState.DELETED.name == task_updates[task.id].state:
                            continue
                        else:
                            task.state = task_updates[task.id].state
                            task.updated_at = task_updates[task.id].updated_at
                    tasks_to_show.append(task)

            # Pretty Print the tasks
            utils.pretty_print(tasks_to_show, self.__task_display_field_list)
        except Exception as e:
            print(f"\nAn error occurred: {e.with_traceback()}")

    def __update_task(self, new_state):
        try:
            #   0. User has any PENDING/COMPLETED tasks
            #   1. Task id can not be empty
            #   2. Task id has to be an integer
            #   3. Task id can not be < 1
            #   4. Task id can not be greater than max task id currently in the system
            #   5. Task id has to be of a task created by the user

            print("\nPlease enter the task id: ")
            while True:
                task_id = input().strip()
                if not task_id:
                    print("\nTask id can not be empty. Please re-enter: ")
                    continue
                try:
                    task_id = int(task_id)  # task_id to be an integer
                except ValueError:
                    print("\nTask id has to be an integer. Please re-enter: ")
                    continue
                if task_id < 1:
                    print("\nTask id can not be less than 1. Please re-enter: ")
                    continue
                if task_id > int(self.__max_task_id):
                    print("\nNo task found. Please re-enter: ")
                    continue
                break

            if task_id in self.__task_update_cache:
                if not bool(self.__task_update_cache[int(task_id)]):
                    print(f"\nTask #{task_id} has already been deleted.")
                else:
                    if TaskState.COMPLETED.name == new_state:
                        print(f"\nTask #{task_id} has already been marked completed.")
                    elif TaskState.DELETED.name == new_state:
                        utils.write(self.__task_update_file_path, 'a',
                                         [task_id, new_state, utils.get_curr_time()],
                                         self.__task_delimiter
                                         )
                        self.__task_update_cache[int(task_id)] = False
                        print(f"\nTask #{task_id} deleted successfully.")
            else:
                utils.write(self.__task_update_file_path, 'a',
                                 [task_id, new_state, utils.get_curr_time()],
                                 self.__task_delimiter
                                 )
                if TaskState.COMPLETED.name == new_state:
                    self.__task_update_cache[int(task_id)] = True
                    print(f"\nTask #{task_id} marked completed.")
                elif TaskState.DELETED.name == new_state:
                    self.__task_update_cache[int(task_id)] = False
                    print(f"\nTask #{task_id} deleted successfully.")

        except Exception as e:
            print(f"\nAn error occurred: {e}")

    def run(self, username):
        while True:
            action_input = TaskManager.get_task_manager_action()
            if action_input == TaskManagerAction.ADD_TASK.value:
                self.__add_task(username)
            elif action_input == TaskManagerAction.LIST_TASKS.value:
                self.__list_tasks(username)
            elif action_input == TaskManagerAction.COMPLETE_TASK.value:
                self.__update_task(TaskState.COMPLETED.name)
            elif action_input == TaskManagerAction.DELETE_TASK.value:
                self.__update_task(TaskState.DELETED.name)
            elif action_input == TaskManagerAction.EXIT.value:
                print("\nUser logged out.")
                break
            else:
                print("\nPlease choose a valid option.")  # Input has to be a valid selection

    @staticmethod
    def get_task_manager_action():
        print("\n\nPlease select any of the options below:\n"
              "\tEnter 1 to add a task\n"
              "\tEnter 2 to view tasks\n"
              "\tEnter 3 to mark a task as completed\n"
              "\tEnter 4 to delete a task\n"
              "\tEnter 5 to logout"
              )
        while True:
            __task_manager_action = input("\nYour selection: ")

            if not isinstance(__task_manager_action, str):  # Input has to be a valid string
                print("\nThe selection was invalid. Please enter a valid string.")
                continue

            try:
                __task_manager_action = int(__task_manager_action)  # Input has to be an integer
            except ValueError:
                print("\nThe selection was invalid. Please enter an integer.")
                continue

            return __task_manager_action
