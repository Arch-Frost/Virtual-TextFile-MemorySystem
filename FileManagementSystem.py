import os
import pickle
from FileClass import File
from DirectoryClass import Directory
from MainMemory import MainMemory
from fiestel_cipher import feistel_encryption, feistel_decryption
from hashing import hash_data
import json

class FileManagementSystem:
    def __init__(self, username, encryption_key):
        self.root = Directory("root")
        self.current_directory = self.root
        self.user = username
        self.encryption_key = encryption_key
        self.files = {}
        self.Memory = MainMemory()
        self.subdirectories = {}

    def create_file(self, name):
        file = File(name)
        self.files[name] = file
        self.current_directory.add_file(file)

    def create_directory(self, name):
        directoryPath = name.split("/")
        current_directory = self.current_directory
        for i in directoryPath:
            if i == "":
                continue
            for directory in current_directory.subdirectories:
                if directory.name == i:
                    current_directory = directory
                    break

        if directoryPath[-1] == "":
            directory = Directory(directoryPath[-2])
        else:
            directory = Directory(directoryPath[-1])

        current_directory.add_subdirectory(directory)
        self.subdirectories[name] = directory

    def delete_file(self, name):
        try:
            current_directory = self.current_directory
            for file in current_directory.files:
                if file.name == name:
                    file.delete(self.Memory)
                    current_directory.remove_file(file)
                    self.files.pop(name)
                    return
        except:
            print("file not found")

    def delete_directory(self, directoryName):
        try:
            directoryPath = directoryName.split("/")

            current_directory = self.current_directory
            for i in directoryPath:
                if i == "":
                    continue
                for directory in current_directory.subdirectories:
                    if directory.name == i:
                        current_directory = directory
                        break
            for file in current_directory.files:
                file.delete(self.Memory)
            current_directory.parent.subdirectories.remove(current_directory)

        except:
            print("directory not found")

    def append_file(self, name, data):
        try:
            file = self.files[name]
            if file.file_size == 0:
                json_data = '{ "text" : "' + data + '", "hash" : ' + json.dumps(hash_data(data)) + ' }'
                encrypted_data = feistel_encryption(json_data, self.encryption_key)
                file.write(encrypted_data, self.Memory)
            else:
                file_data = feistel_decryption(self.readFile(name), self.encryption_key)
                json_data = json.loads(file_data)
                json_data["text"] += " " + data
                json_data["hash"] = hash_data(json_data["text"])
                json_string = '{ "text" : "' + json_data["text"] + '", "hash" : ' + json.dumps(json_data["hash"]) + ' }'
                encrypted_data = feistel_encryption(json_string, self.encryption_key)
                file.write(encrypted_data, self.Memory)
        except KeyError:
            print("The current directory has no such file")
        except:
            print("Something went wrong")

    def print_used_blocks(self):
        self.Memory.print_blocks()

    def write_file(self, name, data):
        try:
            current_directory = self.current_directory
            my_file = current_directory.find_file(name)
            json_data = '{ "text" : "' + data + '", "hash" : ' + json.dumps(hash_data(data)) + ' }'
            encrypted_data = feistel_encryption(json_data, self.encryption_key)
            my_file.write(encrypted_data, self.Memory)
            return my_file
        except Exception as e:
            print(e)
            print("The current directory has no such file")

    def truncate_file(self, name, size):
        try:
            current_directory = self.current_directory
            my_file = current_directory.find_file(name)
            my_file.truncatefile(self.Memory, size)
        except KeyError:
            print("The current directory has no such file")
        except:
            print("Something went wrong")

    def readFile(self, name):
        try:
            current_directory = self.current_directory
            my_file = current_directory.find_file(name)
            if my_file == None:
                print("The current directory has no such file")
            else:
                return my_file.read(self.Memory)
        except KeyError:
            print("The current directory has no such file")
        except ValueError:
            print("The file is empty")
        except:
            print("Something went wrong, file not found")

    def MoveContent(self, name, start, end, newstart):
        try:
            current_directory = self.current_directory
            my_file = current_directory.find_file(name)
            my_file.moveContentWithinFile(self.Memory, start, end, newstart)
        except:
            print("No file found")

    def change_directory(self, name):
        if self.current_directory.parent == None and name == "..":
            return

        if name == "..":
            self.current_directory = self.current_directory.parent
        else:
            pathToDirectory = name.split("/")
            for name in pathToDirectory:
                if name == "":
                    continue
                for directory in self.current_directory.subdirectories:
                    if directory.name == name:
                        self.current_directory = directory
                        break

    def moveFileInDirectory(self, fileName, newDirectory):
        try:
            current_directory = self.current_directory
            my_file = current_directory.find_file(fileName)
            current_directory.remove_file(my_file)
        except:
            print("File not found")
            return

        if newDirectory == "..":
            if current_directory.parent == None:
                return

            current_directory = current_directory.parent
            duplicate = current_directory.find_file(fileName)
            if duplicate != None:
                current_directory.remove_file(duplicate)
                print("Duplicate file found, deleting duplicate")
            current_directory.add_file(my_file)
            return

        newFileDirectory = newDirectory.split("/")
        for i in newFileDirectory:
            if i == "":
                continue
            for directory in current_directory.subdirectories:
                if directory.name == i:
                    current_directory = directory
                    break
        duplicate = current_directory.find_file(fileName)
        if duplicate != None:
            current_directory.remove_file(duplicate)
            print("Duplicate file found, deleting duplicate")
        current_directory.add_file(my_file)

    def passWorkingDirectory(self):
        current_directory = self.current_directory
        path = ""
        while current_directory != None and current_directory.parent is not None:
            path = "/" + current_directory.name + path
            current_directory = current_directory.parent
        if path == "":
            path = "/"
        return path

    def MemoryMap(self, current_directory=None):
        if current_directory is None:
            current_directory = self.root
            print("/")

        spaces = current_directory.level * 2
        for file in current_directory.files:
            blocks = ""
            for block in file.blocks:
                blocks += str(block) + ","
            print(" " * spaces + file.name + " "
                  + str(file.file_size) + " " + blocks)
        for directory in current_directory.subdirectories:
            if directory.name == self.current_directory.name:
                print(" " * spaces + "*" + directory.name + "/")
            else:
                print(" " * spaces + directory.name + "/")
            self.MemoryMap(directory)

    def save(self):
        user_file = os.path.join("users", f"{self.user}.pickle")  
        with open(user_file, "wb") as file:
            pickle.dump(self, file)

    def load(self):
        user_file = os.path.join("users", f"{self.user}.pickle")  
        with open(user_file, "rb") as file:
            return pickle.load(file)

    def listAll(self):
        for i in self.current_directory.subdirectories:
            print(i)
        for i in self.current_directory.files:
            print(i)

    '''
    Adding the Terminal Interface
    '''

    def terminal(self):
        while True:

            prompt = input("\n> ").split(" ")
            command = prompt[0]

            # Exit the terminal: exit
            if command == "exit":
                break

            # Print the help menu: help
            elif command == "help":
                print(
                    """Commands:
                    ls - list all files and directories
                    pwd - print working directory
                    cd - change directory
                    mkdir - make directory
                    rmdir - remove directory
                    touch - create file
                    rm - remove file
                    wr - write to file
                    ap - append to file
                    tr - truncate file
                    mvc - move content within file
                    mvf - move file to another directory
                    cat - read file
                    mmap - show memory map
                    help - show list of commands
                    save - save file system
                    exit - exit terminal
                    """)
                pass

            # List all files and directories in the current directory: ls
            elif command == "ls":
                self.listAll()
                pass

            # Pass the working directory: pwd
            elif command == "pwd":
                print(self.passWorkingDirectory())

            # Change Directory: cd <dirname>
            elif command == "cd":
                if len(prompt) > 1 : self.change_directory(prompt[1])
                pass

            # Create a directory (add to the current directory): mkdir <dirname>
            elif command == "mkdir":
                self.create_directory(prompt[1])
                pass

            elif command == "blocks":
                self.print_used_blocks()

                # Delete a directory (remove from the current directory): rmdir <dirname>
            elif command == "rmdir":
                try:
                    self.delete_directory(prompt[1])
                    pass
                except:
                    print("Directory not found")

            # Create a file (add to the directory): touch <filename>
            elif command == "touch":
                self.create_file(prompt[1])
                pass

            # Delete a file (remove from the directory): rm <filename>
            elif command == "rm":
                self.delete_file(prompt[1])
                pass

            # Write to a file (overwrite): wr <filename> <text>
            elif command == "wr":
                written_text = ""
                for i in range(2, len(prompt)):
                    written_text += prompt[i]
                    if i < len(prompt)-1:
                        written_text += " "
                self.write_file(prompt[1], written_text)

            # Append to a file (add to the end): ap <filename> <text>
            elif command == "ap":
                appended_text = ""
                for i in range(2, len(prompt)):
                    appended_text += prompt[i]
                    if i < len(prompt)-1:
                        appended_text += " "
                self.append_file(prompt[1], appended_text)

            # Truncate a file (remove content): tr <filename> <end bit>
            elif command == "tr":
                try:
                    self.truncate_file(prompt[1], int(prompt[2]))
                except:
                    print("Please enter prompts correctly")

            # Move content within a file: mvc <filename> <start> <size> <newstart/target>
            elif command == "mvc":
                try:
                    self.MoveContent(prompt[1], int(
                        prompt[2]), int(prompt[3]), int(prompt[4]))
                except:
                    print("Please enter prompts correctly")

            # Move a file to a different directory: mvf <filename> <new directory>
            elif command == "mvf":
                self.moveFileInDirectory(prompt[1], prompt[2])

            # Read a file: cat <filename>
            elif command == "cat":
                try:
                    if self.readFile(prompt[1]) != None:
                        file_data = json.loads(feistel_decryption(self.readFile(prompt[1]), self.encryption_key))
                        re_hash = hash_data(file_data["text"])
                        load_hash = file_data["hash"]
                        if re_hash == load_hash:
                            print(file_data["text"])
                        else:
                            print("The file has been corrupted")

                except Exception as e:
                    print(e)
                    print("Please enter prompts correctly")

                pass

            # Show the memory map: mmap
            elif command == "mmap":
                self.MemoryMap()
                pass

            # Save the file system: save
            elif command == "save":
                self.save()

            # Invalid command
            else:
                print("Invalid Command")
                print("Type 'help' for a list of commands")
