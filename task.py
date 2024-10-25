from enum import Enum


class TaskState(Enum):
    PENDING = 1
    COMPLETED = 2
    DELETED = 3


class Task:
    def __init__(self, task_id, user_name=None, desc=None, state=None, created_at=None, updated_at=None):
        self.__id = task_id

        if user_name is not None:
            self.__user_name = user_name

        if desc is not None:
            self.__desc = desc

        if state is not None:
            self.__state = state

        if created_at is not None:
            self.__created_at = created_at

        if updated_at is not None:
            self.__updated_at = updated_at

    # Getter and setter for task_id
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    # Getter and setter for user_name
    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, value):
        self.__user_name = value

    # Getter and setter for desc
    @property
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, value):
        self.__desc = value

    # Getter and setter for state
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    # Getter and setter for created_at
    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        self.__created_at = value

    # Getter and setter for updated_at
    @property
    def updated_at(self):
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, value):
        self.__updated_at = value

    def __str__(self):  # This method overrides string method
        return "{}, {}, {}, {}, {}, {}".format(
            self.__id, self.__user_name, self.__desc, self.__state.name, self.__created_at, self.__updated_at
        )

    @staticmethod
    def field_to_header_mapping():  # This method maps class fields to the display headers in the csv file.
        return [('__id', 'Task Id'), ('__user_name', 'Task Owner'), ('__desc', 'Task Description'),
                ('__state', 'Task State'), ('__created_at', 'Created At'), ('__updated_at', 'Updated At')]
