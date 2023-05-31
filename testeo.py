import cv2 as cv
import numpy as np

paths = ['images\Carbimazole_induced.png',
         'images\Carcinoid_Rare_Koch.png',
         'images\Ovarian_Hyperstimulation.png',
         'images\Malignant_Lymphoma.png',
         'images\pleural_effusion.png']

paths1 = ['images\Clear_Lung_Xray.jpg',
          'images\Frontal_Lung_Xray.png',
          'images\Healthy_Chest_Radiograph.jpg',
          'images/Unremarkable_Chest_Xray.jpg',
          'images/Normal_Pulmonary_RayX.jpg']

# Leer la imagen de la radiografía en escala de grises
image = cv.imread(paths[4], cv.IMREAD_GRAYSCALE)
#redimensionar la imagen a 200 x 200
image = cv.resize(image, (400, 400))
image_aux = cv.imread(paths[4], cv.IMREAD_COLOR)
image_aux = cv.resize(image_aux, (400, 400))

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
    mas_grande = 'izquierda'
else:
    porcentaje = ((altura_derecha / altura_izquierda)-1) * 100
    mas_grande = 'derecha'

#si el porcentaje de la isla mas grande con respecto a la isla mas pequeña es mayor a 50% entonces la imagen esta enferma
if porcentaje > 50:
    print('Enfermo', porcentaje)
else:
    print('Sano', porcentaje)


if mas_grande == 'derecha':
    espejo = np.zeros((400, 400), np.uint8)
    espejo[50:370, 30:200] = image[50:370, 200:370][:, ::-1]
    #obtenemos el pixel blanco con y mas alto de la imagen original
    pixel_mas_alto = left.max()
    #que lo que este menor a ese pixel sea zeros
    espejo[0:pixel_mas_alto+50, 0:200] = 0
elif mas_grande == 'izquierda':
    espejo = np.zeros((400, 400), np.uint8)
    espejo[50:370, 200:370] = image[50:370, 30:200][:, ::-1]
    #obtenemos el pixel blanco con y mas alto de la imagen original
    pixel_mas_alto = right.max()
    #que lo que este menor a ese pixel sea zeros
    espejo[0:pixel_mas_alto+50, 200:370] = 0

#mapa de color a espejo
espejo = cv.applyColorMap(espejo, cv.COLORMAP_WINTER)
#desenfoque a espejo
espejo = cv.GaussianBlur(espejo, (5, 5), 5)
#aplicar contorno a lo rojo

print(image_aux.shape, espejo.shape)

image_aux = cv.addWeighted(image_aux, 1, espejo, 0.5, 0)


cv.imshow('Resultado', image_aux)
cv.imshow('Resultado1', image)



#Mapa de calor
# if mas_grande == 'izquierda':
#     #copiar y pegar la parte izquierda de la imagen en la parte derecha de la imagen en espejo
#     #guardar la imagen espejo
#     espejo = image.copy()
#     espejo[50:370, 200:370] = image[50:370, 30:200][:, ::-1]
#     #aplixcar xor a la imagen espejo entre espejo y la imagen original
#     espejo = cv.bitwise_xor(espejo, image)
#     pixel_mas_bajo_derecha = right.max()
#     print('Pixel mas bajo derecha: ', pixel_mas_bajo_derecha)
    
#     #hacer que desde ese pixel mas bajo hacia arriba todo sea negro
#     espejo[0:pixel_mas_bajo_derecha,0:200] = 0
# elif mas_grande == 'derecha':
#     #copiar y pegar la parte izquierda de la imagen en la parte derecha de la imagen en espejo
#     #guardar la imagen espejo
#     espejo = image.copy()
#     espejo[50:370, 30:200] = image[50:370, 200:370][:, ::-1]
#     #aplixcar xor a la imagen espejo entre espejo y la imagen original
#     espejo = cv.bitwise_xor(espejo, image)
#     pixel_mas_bajo_derecha = left.max()
#     print('Pixel mas bajo derecha: ', pixel_mas_bajo_derecha)
    
#     #hacer que desde ese pixel mas bajo hacia arriba todo sea negro
#     espejo[0:pixel_mas_bajo_derecha,200:370] = 0


#hacer ese if mas elegante






cv.waitKey(0)
cv.destroyAllWindows()
