import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ImageCropper:
    def __init__(self, master, input_folder, output_folder):
        self.master = master
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.image_files = self.get_image_files()
        self.current_image_index = 0

        if not self.image_files:
            print("No images found in the input folder.")
            return

        self.load_image()
        self.setup_ui()

    def get_image_files(self):
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
        return [f for f in os.listdir(self.input_folder) if f.lower().endswith(supported_formats)]

    def load_image(self):
        image_path = os.path.join(self.input_folder, self.image_files[self.current_image_index])
        self.original_image = Image.open(image_path)
        self.scale_image_to_fit_screen()

    def scale_image_to_fit_screen(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        scale_width = screen_width / self.original_image.width
        scale_height = screen_height / self.original_image.height
        scale = min(scale_width, scale_height)

        new_width = int(self.original_image.width * scale)
        new_height = int(self.original_image.height * scale)

        self.image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(self.image)

    def setup_ui(self):
        self.master.attributes('-fullscreen', True)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_center = (screen_width - self.image.width) // 2
        y_center = (screen_height - self.image.height) // 2

        for widget in self.master.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.master, width=self.image.width, height=self.image.height)
        self.canvas.place(x=x_center, y=y_center)

        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

        self.crop_size = min(self.image.width, self.image.height)
        self.crop_square = self.canvas.create_rectangle(0, 0, self.crop_size, self.crop_size, outline='red')

        self.size_slider = ttk.Scale(self.master, from_=50, to=min(self.image.width, self.image.height), orient='horizontal')
        self.size_slider.set(self.crop_size)
        self.size_slider.pack(fill='x', side='bottom')
        self.size_slider.bind('<Motion>', self.update_crop_size)

        self.canvas.bind('<B1-Motion>', self.move_crop_square)
        self.canvas.bind('<Button-1>', self.position_crop_square)
        self.master.bind('<Return>', self.save_and_next_image)

    def update_crop_size(self, event=None):
        self.crop_size = int(self.size_slider.get())
        x1, y1, _, _ = self.canvas.coords(self.crop_square)
        x2 = x1 + self.crop_size
        y2 = y1 + self.crop_size
        if x2 > self.image.width:
            x1 = self.image.width - self.crop_size
            x2 = self.image.width
        if y2 > self.image.height:
            y1 = self.image.height - self.crop_size
            y2 = self.image.height
        self.canvas.coords(self.crop_square, x1, y1, x2, y2)

    def move_crop_square(self, event):
        x1 = max(0, min(event.x - self.crop_size // 2, self.image.width - self.crop_size))
        y1 = max(0, min(event.y - self.crop_size // 2, self.image.height - self.crop_size))
        x2 = x1 + self.crop_size
        y2 = y1 + self.crop_size
        self.canvas.coords(self.crop_square, x1, y1, x2, y2)

    def position_crop_square(self, event):
        x1 = max(0, min(event.x - self.crop_size // 2, self.image.width - self.crop_size))
        y1 = max(0, min(event.y - self.crop_size // 2, self.image.height - self.crop_size))
        x2 = x1 + self.crop_size
        y2 = y1 + self.crop_size
        self.canvas.coords(self.crop_square, x1, y1, x2, y2)

    def save_and_next_image(self, event):
        x1, y1, x2, y2 = map(int, self.canvas.coords(self.crop_square))
        scale_ratio = self.original_image.width / self.image.width
        x1 = int(x1 * scale_ratio)
        y1 = int(y1 * scale_ratio)
        x2 = int(x2 * scale_ratio)
        y2 = int(y2 * scale_ratio)
        cropped_image = self.original_image.crop((x1, y1, x2, y2))
        resized_image = cropped_image.resize((224, 224), Image.LANCZOS)

        output_filename = self.image_files[self.current_image_index]
        output_path = os.path.join(self.output_folder, output_filename)
        resized_image.save(output_path)
        print(f"Image saved as {output_path}")

        self.current_image_index += 1
        if self.current_image_index < len(self.image_files):
            self.load_image()
            self.setup_ui()
        else:
            print("All images processed.")
            self.master.quit()

if __name__ == '__main__':
    input_folder = 'target'
    output_folder = 'result'

    os.makedirs(output_folder, exist_ok=True)

    root = tk.Tk()
    root.title("Image Cropper")
    ImageCropper(root, input_folder, output_folder)
    root.mainloop()