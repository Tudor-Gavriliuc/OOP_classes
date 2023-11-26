import os

class TextFileHandler:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def count_texts(self):
        for file_item in os.listdir(self.folder_path):
            if file_item.endswith("txt"):
                line_count, word_count, char_count = 0, 0, 0
                file_path = os.path.join(self.folder_path, file_item)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()

                lines = text_content.split('\n')
                line_count += len(lines)
                words = text_content.split()
                word_count += len(words)
                char_count += len(text_content)

                print(f"{file_item} - {line_count} lines, {word_count} words, {char_count} characters")
                print("----------------------------------------------------------------------------------")
