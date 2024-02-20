from gui import GUI
from image_loader import ImageLoader
from image_processor import ImageProcessor
from heat_map import HeatMap


class Main:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.heat_map = HeatMap()
        self.image_loader = ImageLoader('images')

    def run(self):
        try:
            self.gui = GUI(self.image_processor, self.image_loader, self.heat_map)
        except Exception as ex:
            print(f"An error ocurred: {ex}")


if __name__ == '__main__':
    try:
        app = Main()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
