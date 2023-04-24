from gui import GUI
from image_loader import ImageLoader


class Main:
    def __init__(self):
        #self.image_processor = ImageProcessor()
        self.image_loader = ImageLoader('images')
        

    def run(self):
        self.gui = GUI(0,self.image_loader)

if __name__ == '__main__':
    app = Main()
    app.run()