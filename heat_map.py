import cv2 as cv
import numpy as np

class HeatMap:
    def __init__(self):
        self.image = None
    
    def get_heatmap(self, image_processed, diagnosis, left, right, path):
        self.image_aux = cv.imread(path, cv.IMREAD_COLOR)
        self.image_aux = cv.resize(self.image_aux, (400, 400))
        self.image = image_processed
        self.diagnosis = diagnosis
   

        if self.diagnosis == 'right':
            espejo = np.zeros((400, 400), np.uint8)
            espejo[50:370, 30:200] = self.image[50:370, 200:370][:, ::-1]
            #obtenemos el pixel blanco con y mas alto de la imagen original
            pixel_mas_alto = left.max()
            #que lo que este menor a ese pixel sea zeros
            espejo[0:pixel_mas_alto+50, 0:200] = 0
        elif self.diagnosis == 'left':
            espejo = np.zeros((400, 400), np.uint8)
            espejo[50:370, 200:370] = self.image[50:370, 30:200][:, ::-1]
            #obtenemos el pixel blanco con y mas alto de la imagen original
            pixel_mas_alto = right.max()
            #que lo que este menor a ese pixel sea zeros
            espejo[0:pixel_mas_alto+50, 200:370] = 0
        
        #mapa de color a espejo
        espejo = cv.applyColorMap(espejo, cv.COLORMAP_RAINBOW)
        #desenfoque a espejo
        espejo = cv.GaussianBlur(espejo, (5, 5), 5)

        self.image_aux = cv.addWeighted(self.image_aux, 0.7, espejo, 0.3, 0)
    
        return self.image_aux
       
        

        