from enum import Enum


class TaskState(Enum):
    PENDING = 1
    COMPLETED = 2
    DELETED = 3


class Task:
    def __init__(self, task_id, user_name=None, desc=None, state=None, created_at=None, updated_at=None):
        self.id = task_id

        if user_name is not None:
            self.user_name = user_name

        if desc is not None:
            self.desc = desc

        if state is not None:
            self.state = state

        if created_at is not None:
            self.created_at = created_at

        if updated_at is not None:
            self.updated_at = updated_at

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}".format(
            self.id, self.user_name, self.desc, self.state.name, self.created_at, self.updated_at
        )

    # TODO: Map these header values to fields using a static map and use that map to refer headers
    # TODO: turn fields to private
    # TODO: instead of 1 single init, see if multiple methods can be made

    @staticmethod
    def get_static_fields():
        return ['Task Id', 'Task Owner', 'Task Description', 'Created At']

    @staticmethod
    def get_variable_fields():
        return ['Task Id', 'Task State', 'Updated At']

    @staticmethod
    def get_printable_fields():
        return ['Task Id', 'Task Description', 'Task State', 'Created At', 'Updated At']

    def get_static_field_values(self):
        return [self.id, self.user_name, self.desc,  self.created_at]

    def get_variable_field_values(self):
        return [self.id, self.state, self.updated_at]
