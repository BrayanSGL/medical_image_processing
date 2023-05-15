from tkinter import *
from PIL import ImageTk, Image


class GUI:
    def __init__(self, image_processor, image_loader, heat_map):
        self.image_processor = image_processor
        self.image_loader = image_loader
        self.heat_map = heat_map
        self.current_image = None
        self.current_heatmap = None

        # Crear la ventana principal
        self.root = Tk()
        # Tamaño de la ventana principal (ancho x alto)
        self.root.geometry("1150x650")
        self.root.resizable(False, False)
        self.root.title("Procesamiento de Imágenes Médicas")
        self.root.iconbitmap('assets/favicon.ico')

        # Crear la barra lateral frame
        self.sidebar = Frame(self.root, width=200,
                             bg='#EAF2F8', height=600, padx=10, pady=10)
        self.sidebar.pack(side=LEFT, fill=BOTH)


        self.preview_canvas = Canvas(self.sidebar, bg='black', width=200, height=200)
        self.preview_canvas.pack(side=TOP, fill=BOTH, expand=True)        

        # Lista de imágenes
        self.image_listbox = Listbox(self.sidebar, width=30, height=20)
        self.image_listbox.pack(side=TOP, fill=BOTH, expand=True)
        self.update_image_listbox()
        self.image_listbox.bind('<<ListboxSelect>>', self.image_selected)

        self.result_label = Label(self.sidebar, text="RESULTADO -> ", bg='#EAF2F8',
                                  fg='black', width=20, height=2, border=1, padx=2, pady=2)
        self.result_label.pack(side=BOTTOM, fill=X)

        # Botón para procesar imágen
        self.load_button = Button(
            self.sidebar, text="Procesar imágen", command=self.process_image, bg='#A9CCE3', fg='black', width=20, height=2, border=1, padx=2, pady=2)
        self.load_button.pack(side=BOTTOM, fill=X)
        self.load_button.config(state=DISABLED)

        # Crear la zona de visualización de imágenes
        self.images_frame = Frame(
            self.root, width=600, height=600, bg='#EAF2F8')
        self.images_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Labels de las imagenes
        self.original_image_label = Label(
            self.images_frame, width=300, height=600, bg='#D4E6F1')
        self.process_image_label = Label(
            self.images_frame, width=300, height=600, bg='#A9CCE3')
        self.heatmap_label = Label(
            self.images_frame, width=300, height=600, bg='#7FB3D5')

        self.original_image_label.grid(
            row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.process_image_label.grid(
            row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.heatmap_label.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        original_image = self.image_loader.image_2_tkinter('assets/prev_one.png')
        self.original_image_label.config(image=original_image)

        process_image = self.image_loader.image_2_tkinter('assets/prev_two.png')
        self.process_image_label.config(image=process_image)

        heatmap = self.image_loader.image_2_tkinter('assets\prev_three.png')
        self.heatmap_label.config(image=heatmap)

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

        # Cargar la imagen seleccionada en la zona de visualización de la barra lateral
        self.current_image = self.image_loader.image_2_tkinter(image_path)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(0, 0, anchor=NW, image=self.current_image)

        # Habilitar el botón de procesar imagen
        self.load_button.config(state=NORMAL)

    def process_image(self):
        # test
        # Obtener el índice del elemento seleccionado en la lista

        print("process_image")

        # Procesar la imagen seleccionada

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
