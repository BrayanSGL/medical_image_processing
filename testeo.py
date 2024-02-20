import cv2 as cv
import numpy as np

paths = ['images/Carbimazole_induced.png',
         'images/Carcinoid_Rare_Koch.png',
         'images/Ovarian_Hyperstimulation.png',
         'images/Malignant_Lymphoma.png',
         'images/pleural_effusion.png']

paths1 = ['images/Clear_Lung_Xray.jpg',
          'images/Frontal_Lung_Xray.png',
          'images/Healthy_Chest_Radiograph.jpg',
          'images/Unremarkable_Chest_Xray.jpg',
          'images/Normal_Pulmonary_RayX.jpg']

image = cv.imread(paths[4], cv.IMREAD_GRAYSCALE)
image = cv.resize(image, (400, 400))
image_aux = cv.imread(paths[4], cv.IMREAD_COLOR)
image_aux = cv.resize(image_aux, (400, 400))

# Image preprocessing
image = cv.GaussianBlur(image, (5, 5), 5)
image = cv.equalizeHist(image)
equalized_image = cv.equalizeHist(image)

# Erosion
kernel = np.ones((3, 3), np.uint8)
dilate_image = cv.dilate(equalized_image, kernel, iterations=1)
eroded_image = cv.erode(dilate_image, kernel, iterations=7)

_, image = cv.threshold(eroded_image, 70, 255, cv.THRESH_BINARY_INV)

frame = np.zeros((400, 400), np.uint8)
frame[50:370, 30:370] = 255

# bitwise and operation
image = cv.bitwise_and(image, frame)

_, labels = cv.connectedComponents(image)

for i in range(1, labels.max() + 1):
    if cv.contourArea(cv.findNonZero(cv.inRange(labels, i, i))) < 200:
        image[labels == i] = 0

print('Cantidad de objetos: ', labels.max())
left = image[50:370, 30:200]
right = image[50:370, 200:370]
left = cv.countNonZero(left)
right = cv.countNonZero(right)

left = image[50:370, 30:200]
right = image[50:370, 200:370]
left = cv.findNonZero(left)
right = cv.findNonZero(right)
left = left[:, 0, 1]
right = right[:, 0, 1]
print('Izquierda: ', left.max(), left.min())
print('Derecha: ', right.max(), right.min())
print('Diferencia izquierda: ', left.max() - left.min())
print('Diferencia derecha: ', right.max() - right.min())

altura_izquierda = left.max() - left.min()
altura_derecha = right.max() - right.min()

if altura_izquierda > altura_derecha:
    porcentaje = ((altura_izquierda / altura_derecha) - 1) * 100
    mas_grande = 'izquierda'
else:
    porcentaje = ((altura_derecha / altura_izquierda) - 1) * 100
    mas_grande = 'derecha'

if porcentaje > 50:
    print('Enfermo', porcentaje)
else:
    print('Sano', porcentaje)

if mas_grande == 'derecha':
    espejo = np.zeros((400, 400), np.uint8)
    espejo[50:370, 30:200] = image[50:370, 200:370][:, ::-1]
    pixel_mas_alto = left.max()
    espejo[0:pixel_mas_alto + 50, 0:200] = 0
elif mas_grande == 'izquierda':
    espejo = np.zeros((400, 400), np.uint8)
    espejo[50:370, 200:370] = image[50:370, 30:200][:, ::-1]
    pixel_mas_alto = right.max()
    espejo[0:pixel_mas_alto + 50, 200:370] = 0

espejo = cv.applyColorMap(espejo, cv.COLORMAP_WINTER)
espejo = cv.GaussianBlur(espejo, (5, 5), 5)

print(image_aux.shape, espejo.shape)

image_aux = cv.addWeighted(image_aux, 1, espejo, 0.5, 0)

cv.imshow('Resultado', image_aux)
cv.imshow('Resultado1', image)

# Mapa de calor
if mas_grande == 'izquierda':
    espejo = image.copy()
    espejo[50:370, 200:370] = image[50:370, 30:200][:, ::-1]
    espejo = cv.bitwise_xor(espejo, image)
    pixel_mas_bajo_derecha = right.max()
    print('Pixel mas bajo derecha: ', pixel_mas_bajo_derecha)

    espejo[0:pixel_mas_bajo_derecha,0:200] = 0
elif mas_grande == 'derecha':
    espejo = image.copy()
    espejo[50:370, 30:200] = image[50:370, 200:370][:, ::-1]
    espejo = cv.bitwise_xor(espejo, image)
    pixel_mas_bajo_derecha = left.max()
    print('Pixel mas bajo derecha: ', pixel_mas_bajo_derecha)
    espejo[0:pixel_mas_bajo_derecha,200:370] = 0

cv.waitKey(0)
cv.destroyAllWindows()
