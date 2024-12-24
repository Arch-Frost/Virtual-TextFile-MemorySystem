import os
import random
import pickle
from hashing import hash_data

class UserSystem:
    def __init__(self, users_folder="users", credentials_file="credentials.pickle"):
        self.users_folder = users_folder
        self.credentials_file = credentials_file
        os.makedirs(users_folder, exist_ok=True)
        
        # Load credentials from the credentials file if it exists
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, "rb") as f:
                self.credentials_data = pickle.load(f)
        else:
            self.credentials_data = {}

    def create_key(self):
        encryption_key = ""
        for _ in range(2048):
            num = random.choice([0, 1])
            encryption_key += str(num)
        return encryption_key

    def create_user(self, username, password):
        # Check if the user already exists in the credentials
        if username in self.credentials_data:
            print("User already exists.")
            return False

        # Generate the user's encryption key and hash the password
        encryption_key = self.create_key()
        hashed_password = hash_data(password)

        # Store user credentials in memory first
        self.credentials_data[username] = {
            "password": hashed_password,
            "encryption_key": encryption_key
        }

        # Save the updated credentials to the credentials.pickle file
        with open(self.credentials_file, "wb") as f:
            pickle.dump(self.credentials_data, f)

        print("User created successfully.")
        return True

    def login_user(self, username, password):
        # Check if the user exists in the credentials file
        if username not in self.credentials_data.keys():
            print("User does not exist.")
            return None

        # Get the stored credentials for the user
        credentials = self.credentials_data[username]

        # Verify the hashed password
        if credentials["password"] == hash_data(password):
            print("Login successful.")
            return {
                "password": credentials["password"],
                "encryption_key": credentials["encryption_key"]
            }
        else:
            print("Invalid password.")
            return None


# Example Usage
if __name__ == "__main__":
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

        elif choice == "3":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")
