class User:
    def __init__(self, user_name, password):
        self.__user_name = user_name
        self.__password = password

    def __str__(self):
        return "{}, {}, {}, {}".format(self.user_name, self.__password)

    @staticmethod
    def get_headers():
        return ['Username', 'Password']
