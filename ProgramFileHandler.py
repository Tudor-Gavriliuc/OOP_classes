import re
import os

class ProgramFileHandler:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def program_processing(self):
        valid_extensions = ("py", "java", "cpp", "c")
        for file_item in os.listdir(self.folder_path):
            if file_item.endswith(valid_extensions):
                line_count, class_count, method_count, word_count, char_count = 0, 0, 0, 0, 0
                file_path = os.path.join(self.folder_path, file_item)
                with open(file_path, 'r', encoding='utf-8') as file:
                    program_content = file.read()

                lines = program_content.split('\n')
                line_count += len(lines)
                class_pattern = r'\bclass\b'
                class_count += len(re.findall(class_pattern, program_content))
                method_pattern = r'\bdef\s+(\w+)\s*\(.*\)\s*:'
                method_count += len(re.findall(method_pattern, program_content))
                words = program_content.split()
                word_count += len(words)
                char_count += len(program_content)

                print(f"{file_item} - {line_count} lines, {class_count} classes, {method_count} methods, {word_count} words, {char_count} characters")
                print("-------------------------------------------------------------------------------------------------------------------------------")
