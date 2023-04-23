import os
from tkinter import *
from PIL import ImageTk, Image

class ImageLoader:
    def __init__(self, images_path, gui):
        self.images_path = images_path
        self.gui = gui
        self.image_list  = []
        self.load_images()

    def load_images(self):
        for filename in os.listdir(self.images_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                self.image_list.append(os.path.join(self.images_path, filename))
        self.gui.update_image_list(self.image_list)

    def load_selected_image(self, index):
        img = Image.open(self.image_list[index])
        self.gui.show_image(img)