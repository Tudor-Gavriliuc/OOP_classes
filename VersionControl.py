from datetime import datetime
import os
from TextFileHandler import TextFileHandler
from ImageFileHandler import ImageFileHandler
from ProgramFileHandler import ProgramFileHandler

class VersionControl:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.text_handler = TextFileHandler(folder_path)
        self.image_handler = ImageFileHandler(folder_path)
        self.program_handler = ProgramFileHandler(folder_path)
        self.snapshot_time = None
        self.files_at_commit = {}
        self.current_files = {}
        self.modified_files = {}
        self.detected_files = []
        self.added_during_commit = {}
        self.deleted_during_commit = {}
        self.detecting_changes = False

    def get_file_info(self):
        files = {}
        for file_item in os.listdir(self.folder_path):
            if os.path.isfile(os.path.join(self.folder_path, file_item)):
                name, extension = file_item.rsplit('.', 1)
                created_time = os.path.getctime(os.path.join(self.folder_path, file_item))
                status = "Unmodified"
                modification_time = os.path.getmtime(os.path.join(self.folder_path, file_item))
                files[file_item] = [name, extension, status, created_time, modification_time]
        return files

    def commit(self):
        self.snapshot_time = datetime.now()
        print("Snapshot time updated to:", self.snapshot_time)
        self.files_at_commit = self.get_file_info()
        self.detecting_changes = True
        self.added_during_commit = {}
        self.deleted_during_commit = {}
        self.modified_files = {}

    def status(self):
        if not self.files_at_commit:
            print("No snapshot has been created yet.")
            return

        self.current_files = self.get_file_info()
        for file_item in self.current_files:
            if file_item not in self.modified_files and self.current_files[file_item][4] > self.files_at_commit[file_item][4]:
                print(f"{file_item} - Modified")
            elif file_item in self.modified_files:
                print(f"{file_item} - Modified")
            else:
                print(f"{file_item} - Unmodified")

        for file_item in self.added_during_commit:
            print(f"{file_item} - New file")
        for file_item in self.deleted_during_commit:
            print(f"{file_item} - Deleted")

    def info(self):
        self.current_files = self.get_file_info()

        while True:
            print("What do you want to display?")
            print("1. All - all files")
            print("2. Image - image files")
            print("3. Text - text files")
            print("4. Program - program files")
            print("5. Go back - go back to main menu")
            print("6. Close - close the program")

            choice_info = input("Enter your choice: ")

            if choice_info == "1":
                for file_item in self.current_files:
                    print(f"Filename - {self.current_files[file_item][0]}")
                    print(f"File extension: {self.current_files[file_item][1]}")
                    print(f"Created time: {self.current_files[file_item][3]}")
                    print(f"Modification time: {self.current_files[file_item][4]}")
                    print("--------------------------------------------------")

            elif choice_info == "2":
                self.image_handler.get_image_size()

            elif choice_info == "3":
                self.text_handler.count_texts()

            elif choice_info == "4":
                self.program_handler.program_processing()

            elif choice_info == "5":
                break

            elif choice_info == "6":
                print("Exiting the program.")
                exit()

            else:
                print("Invalid choice, try again!")

    def detection(self):
        if self.detecting_changes:
            self.current_files = self.get_file_info()
            added_during_commit = {}
            modified_files = {}
            detected_files = []

            file_dict = {
                key: (
                    self.current_files.get(key) or
                    self.added_during_commit.get(key) or
                    self.files_at_commit.get(key)
                ) for key in
                set(self.current_files) | set(self.added_during_commit) | set(self.files_at_commit)
            }

            for file_item in self.current_files:
                if file_item not in self.files_at_commit and file_item not in self.detected_files:
                    print("DETECTION OCCURRED!:")
                    print(f"{file_item} - New file")
                    added_during_commit.update({file_item: self.current_files[file_item]})
                    detected_files.append(file_item)

                elif file_item in self.files_at_commit and file_dict[file_item][4] > self.files_at_commit[file_item][4]:
                    self.files_at_commit[file_item][4] = file_dict[file_item][4]
                    print("DETECTION OCCURRED!:")
                    print(f"{file_item} - Modified")
                    modified_files.update({file_item: self.current_files[file_item]})
                    detected_files.append(file_item)

            deleted_files = set(file_dict.keys()) - set(self.current_files.keys())

            if deleted_files:
                for file_item in deleted_files:
                    if file_item in self.files_at_commit and file_item not in self.deleted_during_commit:
                        self.deleted_during_commit.update({file_item: self.files_at_commit[file_item]})
                        del self.files_at_commit[file_item]
                        print("DETECTION OCCURRED!:")
                        print(f"{file_item} - Deleted")

            self.detected_files += detected_files
            self.added_during_commit.update(added_during_commit)
            self.modified_files.update(modified_files)
