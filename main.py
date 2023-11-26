import threading
import time
from VersionControl import VersionControl

class FolderManager():
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.version_control = VersionControl(folder_path)

    def schedule_detection(self):
        while True:
            self.version_control.detection()
            time.sleep(5)

    def run(self):
        detection_thread = threading.Thread(target=self.schedule_detection)
        detection_thread.daemon = True
        detection_thread.start()

        while True:
            print("What do you want to do?")
            print("1 - Commit")
            print("2 - Status")
            print("3 - Get file info")
            print("4 - Quit the program")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if choice == 1:
                self.version_control.commit()
            elif choice == 2:
                self.version_control.status()
            elif choice == 3:
                self.version_control.info()
            elif choice == 4:
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder you want to manage: ")
    manager = FolderManager(folder_path)
    manager.run()
