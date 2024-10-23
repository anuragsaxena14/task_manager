from enum import Enum
import file_utils


class TaskState(Enum):
    PENDING = 1
    COMPLETED = 2
    DELETED = 3


class Task:
    def __init__(self, task_id, user_name, desc, state=None, created_at=None, updated_at=None):
        self.__id = task_id
        self.__user_name = user_name
        self.__desc = desc
        self.__state = state
        self.__created_at = created_at
        self.__updated_at = updated_at

        if self.__state is None:
            self.__state = TaskState.PENDING

        current_time = file_utils.get_curr_time()
        if self.__created_at is None:
            self.__created_at = current_time

        if self.__updated_at is None:
            self.__updated_at = current_time

    def update(self, state):
        if type(state) is TaskState:
            self.__state = state
            self.__updated_at = file_utils.get_curr_time()
            return True
        else:
            print("The parameter passed is not of type TaskState.")
            return False

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}".format(
            self.__id, self.__user_name, self.__desc, self.__state.name, self.__created_at, self.__updated_at
        )

    @staticmethod
    def get_fields():
        return ['Task Id', 'Task Owner', 'Task Description', 'Task State', 'Created At', 'Updated At']

    def get_values(self):
        return [self.__id, self.__user_name, self.__desc, self.__state.name, self.__created_at, self.__updated_at]
