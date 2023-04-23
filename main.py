from gui import GUI

class Main:
    def __init__(self):
        #self.image_processor = ImageProcessor()
        #self.image_loader = ImageLoader()
        pass

    def run(self):
        self.gui = GUI(0,0)

if __name__ == '__main__':
    app = Main()
    app.run()