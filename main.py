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
        self.gui = GUI(self.image_processor,self.image_loader,self.heat_map)

if __name__ == '__main__':
    app = Main()
    app.run()