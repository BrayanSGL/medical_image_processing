import os

class ImageLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_paths = []
        self.update_image_paths()

    def update_image_paths(self):
        self.image_paths = [os.path.join(self.folder_path, filename) for filename in os.listdir(self.folder_path) if filename.endswith('.jpg')]

    def get_images(self):
        return [os.path.basename(path) for path in self.image_paths]

    def get_image_path(self, index):
        return self.image_paths[index]
