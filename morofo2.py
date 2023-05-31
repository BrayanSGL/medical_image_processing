import cv2
import numpy as np

# Leer la imagen de la radiografía en escala de grises
paths = ['images\PTCL-U_hypereosinophilia.png',
         'images\Paradox_worsening_tuberculosis.png',
         'images\Ovarian_Hyperstimulation.png',
         'images\Carcinoid_Rare_Koch.png',
         'images\Carbimazole_induced.png']


image = cv2.imread(paths[0], cv2.IMREAD_GRAYSCALE)

_, binary_image = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

contours, _ = cv2.findContours(
    opened_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 20]

contour_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(contour_image, filtered_contours, -1, (0, 255, 0), 2)


# Mostrar la imagen original y el resultado
cv2.imshow('Imagen original', image)
cv2.imshow('Resultado', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
