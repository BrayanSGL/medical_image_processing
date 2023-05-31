import cv2
import numpy as np

# Leer la imagen de la radiografía en escala de grises
image = cv2.imread('images\PTCL-U_hypereosinophilia.png', cv2.IMREAD_GRAYSCALE)

# Umbralizar la imagen para obtener una máscara de las regiones negras (aire)
_, binary_image = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)

# Definir el kernel para las operaciones morfológicas
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Aplicar la operación de cierre para cerrar los agujeros en las regiones negras
closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

# Aplicar la operación de apertura para eliminar las pequeñas regiones de aire
opened_image = cv2.morphologyEx(closed_image, cv2.MORPH_OPEN, kernel)

# Mostrar la imagen original y la imagen procesada
cv2.imshow('Imagen original', binary_image)
cv2.imshow('Imagen procesada', opened_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
