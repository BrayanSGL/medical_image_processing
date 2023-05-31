# Procesamiento de Imágenes Médicas
Este repositorio contiene un programa de procesamiento de imágenes médicas que permite detectar y analizar posibles anomalías en los pulmones.

## Requisitos
- Python 3.7 o superior
- Bibliotecas: OpenCV, NumPy, PIL, tkinter

## Instalación
1. Clona este repositorio en tu máquina local:
`git clone https://github.com/tu_usuario/procesamiento-imagenes-medicas.git`
2. Ve al directorio del proyecto:
`cd procesamiento-imagenes-medicas`
3. Instala las dependencias:
`pip install -r requirements.txt`

## Uso
1. Asegúrate de tener las imágenes médicas que deseas procesar en la carpeta "images" dentro del directorio del proyecto.

2. Ejecuta el siguiente comando para iniciar la aplicación:
`python main.py`

3. La aplicación mostrará una ventana con una lista de imágenes en la barra lateral izquierda.

4. Selecciona una imagen de la lista haciendo clic en ella.

5. Haz clic en el botón "Procesar imagen" para procesar la imagen seleccionada.

6. La aplicación mostrará la imagen original, la imagen procesada y un mapa de calor en la zona de visualización.

7. La etiqueta "RESULTADO ->" mostrará el resultado del análisis de la imagen.

## Funcionalidades

- Procesamiento de imagen: La aplicación realiza varias operaciones de procesamiento en la imagen seleccionada, como redimensionamiento, desenfoque, mejora del contraste, umbralización y eliminación de objetos no deseados.

- Análisis de imagen: La aplicación determina la altura relativa de las islas pulmonares izquierda y derecha y calcula el porcentaje de diferencia entre ellas. Si la diferencia supera el 50%, se considera que el pulmón afectado es el que tiene una altura mayor. Si la diferencia es inferior al 50%, no se detecta ninguna anomalía.

- Mapa de calor: Si se detecta una anomalía en la imagen, la aplicación genera un mapa de calor resaltando el área afectada en el pulmón correspondiente.

## Contribuciones
Las contribuciones son bienvenidas. Si quieres mejorar este proyecto, por favor sigue los siguientes pasos:

1. Crea un fork del repositorio.
2. Crea una rama con el nombre de la nueva funcionalidad o mejora que deseas implementar.
3. Realiza los cambios necesarios en el código.
4. Haz commit de tus cambios.
5. Realiza un push a tu repositorio.
6. Crea una pull request en este repositorio.

## Autores
- [Brayan Snader Galeano Lara](https://github.com/brayansgl)
- [Johan Felipe Perez Pulido](https://github.com/JohanPulido)

## Licencia

Este proyecto se encuentra bajo la Licencia MIT. Para más información, por favor consulta el archivo [LICENSE](LICENSE).

## Banco de imagenes utilizado

Se uso Open-i® for Imaging Abstracts, [Open-i®](https://openi.nlm.nih.gov/), para obtener las imagenes de pulmones con derrame pleural.
