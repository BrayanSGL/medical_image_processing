from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

class GUI:
    def __init__(self, image_processor, image_loader):
        self.image_processor = image_processor
        self.image_loader = image_loader
        self.current_image = None
        self.current_heatmap = None
        
        # Crear la ventana principal
        self.root = Tk()
        self.root.title("Procesamiento de Imágenes Médicas")
        
        # Crear la barra lateral
        self.image_listbox = Listbox(self.root)
        self.image_listbox.pack(side=LEFT, fill=Y)
        #self.update_image_listbox()
        #self.image_listbox.bind('<<ListboxSelect>>', self.image_selected)
        
        # Crear la zona de visualización de imágenes
        self.canvas = Canvas(self.root, width=600, height=600)
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Crear el botón para procesar imágenes
        self.process_button = Button(self.root, text="Procesar Imagen", state=DISABLED, command=self.process_image)
        self.process_button.pack(side=BOTTOM, padx=10, pady=10)
        
        # Mostrar la ventana principal
        self.root.mainloop()
        
    def update_image_listbox(self):
        images = self.image_loader.get_images()
        self.image_listbox.delete(0, END)
        for image in images:
            self.image_listbox.insert(END, image)
            
    def image_selected(self, event):
        # Obtener el índice del elemento seleccionado en la lista
        index = self.image_listbox.curselection()[0]
        
        # Obtener la ruta de la imagen seleccionada
        image_path = self.image_loader.get_image_path(index)
        
        # Cargar la imagen seleccionada en la zona de visualización
        self.current_image = Image.open(image_path)
        self.current_image = self.current_image.resize((600, 600))
        self.current_image = ImageTk.PhotoImage(self.current_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=NW, image=self.current_image)
        
        # Habilitar el botón de procesar imagen
        self.process_button.config(state=NORMAL)
        
    def process_image(self):
        pass
        # # Procesar la imagen seleccionada
        # processed_image, heatmap = self.image_processor.process_image(self.current_image)
        
        # # Mostrar la imagen procesada en la zona de visualización
        # self.current_image = ImageTk.PhotoImage(processed_image)
        # self.canvas.delete("all")
        # self.canvas.create_image(0, 0, anchor=NW, image=self.current_image)
        
        # # Mostrar el mapa de calor
        # self.current_heatmap = ImageTk.PhotoImage(heatmap)
        # self.canvas.create_image(0, 0, anchor=NW, image=self.current_heatmap)
        
        # # Deshabilitar el botón de procesar imagen
        # self.process_button.config(state=DISABLED)

