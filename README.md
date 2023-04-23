- ImageProcessor: esta clase será responsable de procesar las imágenes médicas utilizando la librería OpenCV. Tendrá métodos para cargar una imagen, aplicar filtros, detectar patologías y generar un mapa de calor.

- ImageLoader: esta clase manejará la carga de imágenes desde la carpeta 'images' y la actualización de la barra lateral en la interfaz gráfica.

- HeatMap: esta clase se encargará de generar y mostrar el mapa de calor de una imagen procesada.

- GUI: esta clase será responsable de la creación de la interfaz gráfica utilizando la librería Tkinter. Tendrá métodos para manejar la selección de imágenes, llamar al procesamiento de imágenes y actualizar la visualización de la imagen y el mapa de calor.

- Main: esta clase iniciará la aplicación y creará una instancia de la clase GUI.

Cada una de estas clases tendrá atributos y métodos específicos para llevar a cabo su tarea y colaborar con las demás clases en el proyecto. Al utilizar la programación orientada a objetos, se pueden diseñar clases con alta cohesión y bajo acoplamiento, lo que resultará en un código más legible, mantenible y escalable.