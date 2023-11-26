from PIL import Image
import os

class ImageFileHandler:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_image_size(self):
        for file_item in os.listdir(self.folder_path):
            if file_item.endswith(("png", "jpg")):
                try:
                    with Image.open(os.path.join(self.folder_path, file_item)) as img:
                        width, height = img.size
                        print(f"{file_item} - {width}x{height}")
                        print("--------------------------------------------------")
                except Exception as e:
                    print(f"Error: {str(e)}")
