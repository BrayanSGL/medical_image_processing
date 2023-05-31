import cv2 as cv
import numpy as np

paths = ['images\chan1.png',
         'images\PMC2954381_ATM-5-247-g001.png',
         'images\Ovarian_Hyperstimulation.png',
         'images\Carcinoid_Rare_Koch.png',
         'images\Carbimazole_induced.png']

paths1 = ['images\sana1.png',
          'images\sana2.jpg',
          'images\sana3.jpg',
          'images\sana4.jpg',
          'images\sana5.jpg']

# Leer la imagen de la radiografía en escala de grises
image = cv.imread(paths[4], cv.IMREAD_GRAYSCALE)
#redimensionar la imagen a 200 x 200
image = cv.resize(image, (400, 400))

# Preprocesamiento de la imagen
#suavizar la imagen
image = cv.GaussianBlur(image, (5, 5), 5) # (5, 5) es el tamaño del kernel , 0 es la desviacion estandar
#contrastar la imagen
image = cv.equalizeHist(image)
# estiramiento del histograma
equalized_image = cv.equalizeHist(image)

# Erosión
kernel = np.ones((3, 3), np.uint8)  # Elemento estructurante
dilate_image = cv.dilate(equalized_image, kernel, iterations=1) 
eroded_image = cv.erode(dilate_image, kernel, iterations=7)

#umabrasilar la imagen a la inversa
_, image = cv.threshold(eroded_image, 70, 255, cv.THRESH_BINARY_INV) 

frame = np.zeros((400, 400), np.uint8)
frame[50:370, 30:370] = 255

#operacion and
image = cv.bitwise_and(image, frame)

#detectar la canridad de objetos en la imagen por medio de un metodo de tiquetado en busquda a profundidad
_, labels = cv.connectedComponents(image)
#contar la cantidad de objetos

#Elimirnar el objetu cuya area sea menor a 20 pixeles
for i in range(1, labels.max() + 1):
    if cv.contourArea(cv.findNonZero(cv.inRange(labels, i, i))) < 200:
        image[labels == i] = 0

print('Cantidad de objetos: ', labels.max())
#Detectar que isla es mas grande la de la izquierda o la de la derecha
left = image[50:370, 30:200]
right = image[50:370, 200:370]
left = cv.countNonZero(left)
right = cv.countNonZero(right)

#detartar el pixel blanco mas alto de la imagen a la izquierda y a la derecha y el pixel mas bajo de la imagen a la izquierda y a la derecha
left = image[50:370, 30:200]
right = image[50:370, 200:370]
left = cv.findNonZero(left)
right = cv.findNonZero(right)
left = left[:, 0, 1]
right = right[:, 0, 1]
print('Izquierda: ', left.max(), left.min())
print('Derecha: ', right.max(), right.min())
#calcular la diferencia entre el pixel mas alto y el pixel mas bajo de la imagen a la izquierda y a la derecha
print('Diferencia izquierda: ', left.max() - left.min())
print('Diferencia derecha: ', right.max() - right.min())

altura_izquierda = left.max() - left.min()
altura_derecha = right.max() - right.min()

#porcentaje de tamaño de la isla mas grande con respecto a la isla mas pequeña
if altura_izquierda > altura_derecha:
    porcentaje = ((altura_izquierda / altura_derecha)-1) * 100
else:
    porcentaje = ((altura_derecha / altura_izquierda)-1) * 100

#si el porcentaje de la isla mas grande con respecto a la isla mas pequeña es mayor a 50% entonces la imagen esta enferma
if porcentaje > 50:
    print('Enfermo', porcentaje)
else:
    print('Sano', porcentaje)


#mostrar la imagen procesada


cv.imshow('Resultado', image)
cv.imshow('Resultado1', equalized_image)

cv.waitKey(0)
cv.destroyAllWindows()
