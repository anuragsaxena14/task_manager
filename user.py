class User:
    def __init__(self, user_name, password):
        self.__user_name = user_name
        self.__password = password

    def __str__(self):  # This method overrides string method
        return "{}, {}".format(self.__user_name, self.__password)

    @staticmethod
    def field_to_header_mapping():  # This method maps class fields to the display headers in the csv file.
        return [('__user_name', 'Username'), ('__password', 'Password')]
