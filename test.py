from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Mostrando imagen en Label")

# Cargar la imagen desde la ruta del archivo
def resize_to_square(image):
    width, height = image.size
    size = max(width, height)
    new_image = Image.new('RGB', (size, size), (0, 0, 0))
    new_image.paste(image, ((size - width) // 2, (size - height) // 2))
    return new_image

image_path = "images/brain6.jpg"
image = Image.open(image_path)
# ajustar el tamaño de la imagen
image = resize_to_square(image)
# Convertir la imagen para que pueda ser mostrada en Tkinter
image = image.resize((300, 300))
tk_image = ImageTk.PhotoImage(image)

# Crear un label y agregar la imagen
label = Label(root, image=tk_image)
label.pack()



root.mainloop()