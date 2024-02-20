from PIL import Image, ImageTk
import os


class ImageLoader:
    # initialization of the class instance with the specified folder path
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_paths = []
        self.images = []  # Store references to ImageTk.PhotoImage objects
        # update of the list of image paths
        self.update_image_paths()

    # list files in the specified folder
    def update_image_paths(self):
        self.image_paths = [os.path.join(self.folder_path, filename) for filename in os.listdir(self.folder_path) if
                            (filename.endswith('.jpg') or filename.endswith('.png'))]
        print("Image Paths:", self.image_paths)

    # list files names
    def get_images(self):
        return [os.path.basename(path) for path in self.image_paths]

    # full path of the image at specific indexes
    def get_image_path(self, index):
        return os.path.join(self.folder_path, os.path.basename(self.image_paths[index]))

    @staticmethod
    def resize_to_square(image):
        # adding a black border if necessary
        width, height = image.size  # extract image dimensions
        size = max(width, height)   # ensuring the square to be large enough
        new_image = Image.new('RGB', (size, size), (0, 0, 0))
        # horizontal offset to center the image within the square calculation
        x_offset = (size - width) // 2
        y_offset = (size - height) // 2  # vertical offset
        # original image onto the new image at the centered position
        new_image.paste(image, (x_offset, y_offset))
        return new_image

    @staticmethod
    def image_2_tkinter(image_path):
        try:
            image = Image.open(image_path)
            print("Image size before:", image.size)
            image = ImageTk.PhotoImage(image)
            print("Image size after:", image.width(), image.height())
            # Tkinter PhotoImage return used for displaying the image in the GUI
            return image
        except Exception as e:
            print(f"Error loading image from {image_path}: {e}")
            return None
