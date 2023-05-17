import os
from PIL import Image, ImageTk

class ImageLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_paths = []
        self.update_image_paths()

    def update_image_paths(self):
        self.image_paths = [os.path.join(self.folder_path, filename) for filename in os.listdir(self.folder_path) if (filename.endswith('.jpg') or filename.endswith('.png'))]

    def get_images(self):
        return [os.path.basename(path) for path in self.image_paths]

    def get_image_path(self, index):
        return self.image_paths[index]
    
    def resize_to_square(self,image):
        width, height = image.size
        size = max(width, height)
        new_image = Image.new('RGB', (size, size), (0, 0, 0))
        new_image.paste(image, ((size - width) // 2, (size - height) // 2))
        return new_image

    def image_2_tkinter(self,image_path):
        image = Image.open(image_path)
        image = self.resize_to_square(image)
        image = image.resize((200, 200))
        image = ImageTk.PhotoImage(image)
        return image
