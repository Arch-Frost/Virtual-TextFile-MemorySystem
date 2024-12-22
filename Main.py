from FileManagementSystem import *  
from UserSystem import *


def login_system():
    user_system = UserSystem()

    while True:
        print("\n1. Create User\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_system.create_user(username, password)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_data = user_system.login_user(username, password)
            if user_data:
                print(f"Welcome, {username}!")
                return username, user_data["encryption_key"]

        elif choice == "3":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


def create_file_system(file_system):
    print("Creating new file system...\n")
    file_system.create_file("fileInRoot.txt")
    file_system.create_directory("dir1")
    file_system.change_directory("dir1")
    file_system.create_file("fileInDir1.txt")       
    file_system.create_directory("dir2")
    file_system.change_directory("dir2")
    file_system.create_file("fileInDir2.txt")

    file_system.write_file("fileInDir2.txt", "Hello World")
    file_system.change_directory("..")
    file_system.change_directory("..")
    file_system.save()

def main(): 
    username, encryption_key = login_system()
    if username is None:
        return
    else:
        file_system = FileManagementSystem(username, encryption_key)
        if os.path.exists(f"users//{username}.pickle"):
            print("Loading file system...\n")
            file_system = file_system.load()

        else:
            create_file_system(file_system)
    
        file_system.MemoryMap()
        file_system.terminal()


main()
