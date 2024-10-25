from auth_manager import AuthManager
from task_manager import TaskManager

if __name__ == "__main__":

    print("\n\n#######################################")
    print("#                Welcome!             #")
    print("#######################################")
    auth_manager = AuthManager()  # Start the auth manager
    username = auth_manager.run()  # Auth manager will return an authenticated username
    if username:  # No username means auth failed or the user chose to exit
        task_manager = TaskManager()
        task_manager.run(username)  # Start the task manager
    print("\n\n#######################################")
    print("#                GoodBye!             #")
    print("#######################################\n")
