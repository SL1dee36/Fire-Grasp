import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
import customtkinter as ctk

WINDOW_WIDHT = 1280
WINDOW_HEIGHT = 720

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()
        self.drawn_pixels = []

    def create_widgets(self):

        self.LeftFrame = ctk.CTkFrame(self,width=320,height=WINDOW_HEIGHT,corner_radius=0)
        self.LeftFrame.pack(padx=0,pady=0,side="left")
        self.LeftFrame.pack_propagate(0)

        self.RightFrame = ctk.CTkFrame(self,width=960,height=WINDOW_HEIGHT,corner_radius=0)
        self.RightFrame.pack(padx=0,pady=0,side="left")
        self.RightFrame.pack_propagate(0)

        self.load = ctk.CTkButton(self.LeftFrame, text="Загрузить изображение", command=self.load_image)
        self.load.pack(padx=5,pady=5,side="top")

        self.default = ctk.CTkButton(self.LeftFrame, text="Использовать default.png", command=self.load_default)
        self.default.pack(padx=5,pady=5,side="top")

        self.save = ctk.CTkButton(self.LeftFrame, text="Сохранить данные огня", command=self.save_fire_data)
        self.save.pack(padx=5,pady=5,side="top")

        # Создаем холст с центрированием
        self.canvas = tk.Canvas(self.RightFrame, width=950, height=530)
        self.canvas.pack(padx=5,pady=5)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.output = ctk.CTkTextbox(self.RightFrame,width=960,height=170)
        self.output.pack(padx=5,pady=5)

    def load_image(self):
        filepath = filedialog.askopenfilename()
        self.display_image(filepath)
        self.output.delete("0.0", "end")
        self.output.insert("0.0", f"\n\tImage: {filepath} uploaded!\n\tPlease draw the outline of the fire")
    def load_default(self):
        self.display_image("tools\\images\\default.png")
        self.output.delete("0.0", "end")
        self.output.insert("0.0", f"\n\tImage: default.png uploaded!\n\tPlease draw the outline of the fire")

    def display_image(self, filepath):
        self.image = Image.open(filepath)
        # Изменить размер изображения
        self.image = self.image.resize((950, 530), Image.Resampling.LANCZOS)

        # Сохраните измененное изображение
        self.image.save('tools\\images\\edited_image.png') 

        self.cv_image = cv2.imread('tools\\images\\edited_image.png')

        self.tk_image = ImageTk.PhotoImage(self.image)
        if hasattr(self, 'canvas_image'):
            self.canvas.delete(self.canvas_image)
        self.canvas_image = self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

    def draw(self, event):
        # Получаем координаты относительно левого верхнего угла холста
        x = event.x
        y = event.y

        # Проверяем, находится ли точка в пределах холста
        if 0 <= x <= 950 and 0 <= y <= 530: 
            if self.cv_image is not None:
                self.cv_image[event.y, event.x] = [0, 0, 0]  # Mark this pixel as black in the cv_image
                self.canvas.create_oval(event.x - 6, event.y - 6, event.x + 6, event.y + 6, fill='black')
                self.drawn_pixels.append((event.y, event.x))

    def save_fire_data(self):
        if self.cv_image is not None and self.drawn_pixels is not None:
            fire_mask = self.get_fire_mask(self.cv_image, self.drawn_pixels)
            fire_pixels = self.cv_image[fire_mask]
            fire_data = cv2.cvtColor(fire_pixels.reshape(-1, 1, 3), cv2.COLOR_BGR2HSV)

            # Игнорировать черный цвет
            fire_data = fire_data[~np.all(fire_data == [0, 0, 0], axis=-1)]
            #Дополнительная проверка валидности:

            lower = np.min(fire_data, axis=0) if len(fire_data) > 0 else [5, 65, 145]
            if lower is not None and all(l <= u for l, u in zip(lower, [0, 65, 150])):
                lower = [0, 65, 150]
                if lower[-1] < 150:
                    lower = [0, 200, 100]

            upper = np.max(fire_data, axis=0) if len(fire_data) > 0 else None  # Максимальное значение не изменяется
            if upper is not None and all(l <= u for l, u in zip(upper, [30, 255, 255])):
                upper = [15, 255, 255]
                if upper[-3] > 40:
                    upper = [30, 255, 255]
 
            with open("tools\\FireDatas.txt", "w") as f:
                f.write(f"{lower if lower is not None else '[0, 65, 150]'}\n")
                f.write(f"{upper if upper is not None else '[30, 255, 255]'}\n")
                print(f'Saved!\n\n{lower}\n{upper}')

                self.output.delete("0.0", "end")
                self.output.insert("0.0", f"\n\tFire Detected!\n\tLOW: {lower if lower is not None else '[0, 65, 150]'}\n\tHIGH: {upper if upper is not None else '[30, 255, 255]'}\n\n\tYou can use the sliders in the debug menu, to change the fire detection parameters\n\tФайл содержащий данные: 'tools/FireDatas.txt'") 

    def get_fire_mask(self, image, pixels):
        mask = np.zeros(image.shape[:2], dtype=bool)
        mask[tuple(zip(*pixels))] = True
        return mask

    def get_neighbors(self, pixel, shape):
        y, x = pixel
        neighbors = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
        return [p for p in neighbors if 0 <= p[0] < shape[0] and 0 <= p[1] < shape[1]]

root = tk.Tk()
root.geometry(f"{WINDOW_WIDHT}x{WINDOW_HEIGHT}")
root.resizable(False,False)
app = Application(master=root)
app.mainloop()