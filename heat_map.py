import cv2 as cv
import numpy as np


class HeatMap:
    def __init__(self):
        self.image_aux = None
        self.diagnosis = None
        self.image = None
        self.espejo = None

    def get_heatmap(self, image_processed, diagnosis, left, right, path):
        # original image from the given path reading .
        self.image_aux = cv.imread(path, cv.IMREAD_COLOR)
        # and resizing it to 400x400
        self.image_aux = cv.resize(self.image_aux, (400, 400))
        self.image = image_processed
        self.diagnosis = diagnosis

        if self.diagnosis == 'right':
            espejo = np.zeros((400, 400), np.uint8)  # array filled with zeros creation
            espejo[50:370, 30:200] = self.image[50:370, 200:370][:, ::-1]  # mirror effect
            # region that effect must be applied: rows (50 to 370) and columns (30 to 200)
            # region to be mirrored: rows (50 to 370) and columns (200 to 370)
            # and reverse the order of elements along the second axis

            # maximum Y-coordinate of White Pixels of the left side
            pixel_mas_alto = left.max()
            # set Pixels Below to zero
            espejo[0:pixel_mas_alto + 50, 0:200] = 0
            # colorMap application
            espejo = cv.applyColorMap(espejo, cv.COLORMAP_RAINBOW)
            # Gaussian blur
            espejo = cv.GaussianBlur(espejo, (5, 5), 5)
            # Weighted addition with no gamma correction (last 0)
            self.image_aux = cv.addWeighted(self.image_aux, 0.7, espejo, 0.3, 0)

        elif self.diagnosis == 'left':
            espejo = np.zeros((400, 400), np.uint8)
            espejo[50:370, 200:370] = self.image[50:370, 30:200][:, ::-1]
            pixel_mas_alto = right.max()
            espejo[0:pixel_mas_alto + 50, 200:370] = 0
            # colorMap application
            espejo = cv.applyColorMap(espejo, cv.COLORMAP_RAINBOW)
            # Gaussian blur
            espejo = cv.GaussianBlur(espejo, (5, 5), 5)
            # Weighted addition with no gamma correction (last 0)
            self.image_aux = cv.addWeighted(self.image_aux, 0.7, espejo, 0.3, 0)


        return self.image_aux
        