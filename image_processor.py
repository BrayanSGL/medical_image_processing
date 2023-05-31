import cv2 as cv
import numpy as np
from PIL import ImageTk, Image

class ImageProcessor():
    def __init__(self) -> None:
        self.image = None

    def process_image(self, path):
        self.image = cv.imread(path, cv.IMREAD_GRAYSCALE)
        if self.image is None:
            print("Could not read input image file")
            return
        self.image = cv.resize(self.image, (400, 400))
        # Preprocesamiento de la imagen
        self.image = cv.GaussianBlur(self.image, (5, 5), 5)
        # contrastar la imagen
        self.image = cv.equalizeHist(self.image)

        # Erosión
        kernel = np.ones((3, 3), np.uint8)  # Elemento estructurante
        dilate_image = cv.dilate(self.image, kernel, iterations=1)
        eroded_image = cv.erode(dilate_image, kernel, iterations=7)

        # umabrasilar la imagen a la inversa
        _, self.image = cv.threshold(
            eroded_image, 70, 255, cv.THRESH_BINARY_INV)

        # creacion de un marco para eliminar los objetos que toquen el marco
        frame = np.zeros((400, 400), np.uint8)
        frame[50:370, 30:370] = 255

        # operacion and
        self.image = cv.bitwise_and(self.image, frame)
        # detectar la canridad de objetos en la imagen
        _, labels = cv.connectedComponents(self.image)

        # Elimirnar el objetu cuya area sea menor a 200 pixeles
        for i in range(1, labels.max() + 1):
            if cv.contourArea(cv.findNonZero(cv.inRange(labels, i, i))) < 200:
                self.image[labels == i] = 0
        
        return self.image

    def get_diagnosis(self):

        # Detectar que isla es mas alta la de la izquierda o la de la derecha
        left = self.image[50:370, 30:200]
        right = self.image[50:370, 200:370]
        left = cv.findNonZero(left)
        right = cv.findNonZero(right)
        left = left[:, 0, 1]
        right = right[:, 0, 1]

        higth_left = left.max() - left.min()
        higth_right = right.max() - right.min()

        if higth_left > higth_right:
            percentage = ((higth_left/higth_right) - 1) * 100
            affected_lung = 'left'
        elif higth_right > higth_left:
            percentage = ((higth_right/higth_left) - 1) * 100
            affected_lung = 'right'
        else:
            percentage = 0
            affected_lung = 'none'

        return True if percentage > 50 else False, round(percentage, 1), affected_lung, left, right

    def cv_2_tkinter(self, image):
        # resize image
        image = cv.resize(image, (200, 200))
        img_pil = Image.fromarray(image)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        return img_tk