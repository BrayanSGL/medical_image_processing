import tkinter as tk
import threading


class GUI:
    def __init__(self, image_processor, image_loader, heat_map):
        self.image_processor = image_processor
        self.image_loader = image_loader
        self.heat_map = heat_map
        self.current_image = None
        self.current_original = None
        self.current_heatmap = None
        self.current_processed = None
        self.current_diagnosis = None

        # Main window initialization
        self.root = tk.Tk()
        # size (width x height)
        self.root.geometry("1150x650")
        self.root.resizable(False, False)
        self.root.title("Digital Image Processing")
        self.root.iconbitmap('assets/favicon.ico')

        # sidebar frame creation
        self.sidebar = tk.Frame(self.root, width=200, bg='#A9CCE3', height=600, padx=10, pady=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH)

        self.preview_canvas = tk.Canvas(self.sidebar, bg='white', width=200, height=200)
        print(f"Initial Canvas size: {self.preview_canvas.winfo_width()} {self.preview_canvas.winfo_height()}")
        self.preview_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # List of images
        self.image_listbox = tk.Listbox(self.sidebar, width=40, height=20, bg='yellow')
        self.image_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.update_image_listbox()
        self.image_listbox.bind('<<ListboxSelect>>', self.image_selected)

        # Button to process image
        self.load_button = tk.Button(self.sidebar, text="Load image", command=self.process_image_threaded,
                                     bg='#A9CCE3', fg='black', width=20, height=4, border=1, padx=2, pady=2)
        self.load_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.load_button.config(state=tk.DISABLED)

        # Result label
        self.result_label = tk.Label(self.sidebar, text="RESULTADO -> ", bg='#A9CCE3', fg='black', width=20, height=2,
                                     border=1, padx=2, pady=2)
        self.result_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_label.config(state=tk.DISABLED)

        # Create the image display frame
        self.images_frame = tk.Frame(self.root, width=300, height=300, bg='#A9CCE3')
        self.images_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Labels for images
        aspect_ratio = 4 / 3
        label_height = 200
        label_width = int(label_height * aspect_ratio)

        self.original_image_label = tk.Label(self.images_frame, width=label_width, height=label_height, bg='#D4E6F1')
        self.process_image_label = tk.Label(self.images_frame, width=label_width, height=label_height, bg='#A9CCE3')
        self.heatmap_label = tk.Label(self.images_frame, width=label_width, height=label_height, bg='#7FB3D5')

        self.original_image_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.process_image_label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.heatmap_label.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # Show the main window
        self.root.mainloop()

    def update_image_listbox(self):
        images = self.image_loader.get_images()
        self.image_listbox.delete(0, tk.END)
        for image in images:
            self.image_listbox.insert(tk.END, image)

    def image_selected(self, event):
        print("Image selected!")

        try:
            # Get the index of the selected item in the list
            index = self.image_listbox.curselection()[0]
            # Get the path of the selected image
            image_path = self.image_loader.get_image_path(index)
            # Print the image path for debugging
            print("Loading image:", image_path)
            # Load the selected image into the sidebar preview canvas
            self.current_image = self.image_loader.image_2_tkinter(image_path)
            # Clear previous drawings on the canvas
            self.preview_canvas.delete("all")
            # Create the new image on the canvas
            self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
            self.preview_canvas.config(width=self.current_image.width(), height=self.current_image.height())
            # Enable the process image button
            self.load_button.config(state=tk.NORMAL)
            print(f"Canvas size: {self.preview_canvas.winfo_width()} {self.preview_canvas.winfo_height()}")

            # Display the original image immediately
            self.current_original = self.image_loader.image_2_tkinter(image_path)
            self.original_image_label.config(image=self.current_original)

        except IndexError:
            print("No image selected.")

    def process_image_threaded(self):
        # Create a thread for processing the image
        threading.Thread(target=self.process_image).start()

    def process_image(self):
        try:
            # Process the selected image
            index = self.image_listbox.curselection()[0]
            image_path = self.image_loader.get_image_path(index)

            print("Processing image:", image_path)

            # Print label size and position before configuration
            print("Label size before:", self.original_image_label.winfo_width(),
                  self.original_image_label.winfo_height())
            print("Label position before:", self.original_image_label.winfo_x(), self.original_image_label.winfo_y())

            # Load the original image
            self.current_original = self.image_loader.image_2_tkinter(image_path)
            print("Original image loaded")

            # Print label size and position
            print("Label size:", self.original_image_label.winfo_width(), self.original_image_label.winfo_height())
            print("Label position:", self.original_image_label.winfo_x(), self.original_image_label.winfo_y())

            # Configure the original image label
            self.original_image_label.config(image=self.current_original)
            print("Original image label configured")

            # Process the image
            image_processed = self.image_processor.process_image(image_path)

            # Convert the processed image to Tkinter format
            self.current_processed = self.image_processor.cv_2_tkinter(image_processed)

            # Configure the processed image label
            self.process_image_label.config(image=self.current_processed)
            print("Processed image label configured")

            # Get the diagnosis
            self.current_diagnosis = self.image_processor.get_diagnosis()

            # Convert from boolean to string
            if self.current_diagnosis[0]:
                diagnosis = "Afirmativo | " + str(self.current_diagnosis[2]) + " | " + str(
                    self.current_diagnosis[1]) + "%"
            else:
                diagnosis = "Negativo"

            # Configure the result label
            self.result_label.config(text="-> " + diagnosis)
            print("Result label configured")

            # Configure the heatmap label if the diagnosis is affirmative
            if self.current_diagnosis[0]:
                self.current_heatmap = self.heat_map.get_heatmap(image_processed,
                                                                 self.current_diagnosis[2],
                                                                 self.current_diagnosis[3],
                                                                 self.current_diagnosis[4],
                                                                 image_path)
                self.current_heatmap = self.image_processor.cv_2_tkinter(self.current_heatmap)
                self.heatmap_label.config(image=self.current_heatmap)
                print("Heatmap label configured")

        except IndexError:
            print("No image selected.")

        finally:

            # Schedule GUI update after processing
            self.root.after(1, self.update_gui_after_processing)

    def update_gui_after_processing(self):
        # Enable the process image button after processing
        self.load_button.config(state=tk.NORMAL)
        # GUI update
        self.root.update()
