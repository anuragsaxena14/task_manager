from enum import Enum
import utils
from user import User
import hashlib


class AuthenticationMode(Enum):
    LOGIN = 1
    REGISTER = 2
    NONE = 3


class AuthManager:

    # This file would store the user details like username, password.
    __user_file_path = "./user.csv"
    __user_delimiter = "|"

    # ['Username','Password']
    __user_display_field_list = [User.field_to_header_mapping()[0][1], User.field_to_header_mapping()[1][1]]

    def __init__(self):
        try:
            is_user_file_present = utils.is_file_present(self.__user_file_path)
            create_user_file = (not is_user_file_present) or utils.is_file_empty(self.__user_file_path)
            if create_user_file:
                # Create user.csv with headers
                utils.write(self.__user_file_path, 'w', self.__user_display_field_list, self.__user_delimiter)
        except Exception as e:
            print(f"\nAuth manager initialization failed: {e}")

    def run(self):
        auth_mode = AuthManager.get_auth_mode_input()

        if auth_mode == AuthenticationMode.LOGIN.value:
            return self.__login()
        elif auth_mode == AuthenticationMode.REGISTER.value:
            return self.__register()
        return ""

    def __register(self):
        username = input("Enter a unique username: ")
        if not utils.is_value_unique(self.__user_file_path, self.__user_delimiter,
                                          username, self.__user_display_field_list[0]):
            print("\nUsername already exists. User registration failed.")
            return
        password = input("Enter a password: ")
        hashed_password = self.__hash_password(password)
        utils.write(self.__user_file_path, 'a', [username, hashed_password], self.__user_delimiter)
        print("\nUser registration successful.")
        return username

    def __login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = self.__hash_password(password)
        value_match = self.__match_credentials(username, hashed_password)

        if not bool(value_match[0]): # Matching username
            print(f"\nNo user with username '{username}'. Login failed.")
            return
        elif not bool(value_match[1]):
            print(f"\nPassword '{password} 'did not match. Login failed.")
            return

        print("\nLogin successful!")
        return username

    @staticmethod
    def __hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def __match_credentials(self, username, hashed_password):
        return utils.match_values(self.__user_file_path, self.__user_delimiter,
                                       [username, hashed_password], self.__user_display_field_list)

    @staticmethod
    def get_auth_mode_input():
        print("\n\nPlease select one of the modes below to authenticate:\n"
              "\tEnter 1 to login\n"
              "\tEnter 2 to register\n"
              "\tEnter 3 to exit"
              )
        while True:
            user_input = input("\nYour selection: ")

            if not isinstance(user_input, str):  # Input has to be a valid string
                print("\nThe selection was invalid. Please enter a valid string.")
                continue

            try:
                user_input = int(user_input)  # Input has to be an integer
            except ValueError:
                print("\nThe selection was invalid. Please enter an integer.")
                continue

            for auth_mode in AuthenticationMode:
                if auth_mode.value == user_input:
                    return user_input
            print("\nThe selection was invalid. Please choose a valid option.")

