from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from functions.utils import FIRE_DATA_PATH, save_fire_bounds

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CANVAS_WIDTH = 950
CANVAS_HEIGHT = 530
IMAGES_DIR = ROOT_DIR / "tools" / "Images"


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.drawn_pixels = set()
        self.clean_cv_image = None
        self.tk_image = None
        self.canvas_image = None
        self.create_widgets()

    def create_widgets(self):
        self.LeftFrame = ctk.CTkFrame(self, width=320, height=WINDOW_HEIGHT, corner_radius=0)
        self.LeftFrame.pack(padx=0, pady=0, side="left")
        self.LeftFrame.pack_propagate(False)

        self.RightFrame = ctk.CTkFrame(self, width=960, height=WINDOW_HEIGHT, corner_radius=0)
        self.RightFrame.pack(padx=0, pady=0, side="left")
        self.RightFrame.pack_propagate(False)

        self.load = ctk.CTkButton(self.LeftFrame, text="Загрузить изображение", command=self.load_image)
        self.load.pack(padx=5, pady=5, side="top")

        self.default = ctk.CTkButton(self.LeftFrame, text="Использовать default.png", command=self.load_default)
        self.default.pack(padx=5, pady=5, side="top")

        self.save = ctk.CTkButton(self.LeftFrame, text="Сохранить данные огня", command=self.save_fire_data)
        self.save.pack(padx=5, pady=5, side="top")

        self.canvas = tk.Canvas(self.RightFrame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack(padx=5, pady=5)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.output = ctk.CTkTextbox(self.RightFrame, width=960, height=170)
        self.output.pack(padx=5, pady=5)

    def load_image(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        self.display_image(Path(filepath))
        self.output.delete("0.0", "end")
        self.output.insert("0.0", f"\n\tImage: {filepath} uploaded!\n\tPlease draw the outline of the fire")

    def load_default(self):
        default_path = IMAGES_DIR / "default.png"
        self.display_image(default_path)
        self.output.delete("0.0", "end")
        self.output.insert("0.0", "\n\tImage: default.png uploaded!\n\tPlease draw the outline of the fire")

    def display_image(self, filepath):
        self.drawn_pixels.clear()
        self.canvas.delete("stroke")

        image = Image.open(filepath).convert("RGB")
        image = image.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.Resampling.LANCZOS)

        edited_path = IMAGES_DIR / "edited_image.png"
        image.save(edited_path)
        self.clean_cv_image = cv2.imread(str(edited_path))

        self.tk_image = ImageTk.PhotoImage(image)
        if self.canvas_image is not None:
            self.canvas.delete(self.canvas_image)
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def draw(self, event):
        x, y = event.x, event.y
        if 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT and self.clean_cv_image is not None:
            self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill="black", outline="black", tags="stroke")
            self.drawn_pixels.add((y, x))

    def save_fire_data(self):
        if self.clean_cv_image is None or not self.drawn_pixels:
            self.output.delete("0.0", "end")
            self.output.insert("0.0", "\n\tLoad an image and draw over the fire first!")
            return

        ys, xs = zip(*self.drawn_pixels)
        fire_pixels = self.clean_cv_image[np.array(ys), np.array(xs)]
        fire_hsv = cv2.cvtColor(fire_pixels.reshape(-1, 1, 3), cv2.COLOR_BGR2HSV).reshape(-1, 3)

        lower = np.min(fire_hsv, axis=0).tolist()
        upper = np.max(fire_hsv, axis=0).tolist()

        save_fire_bounds(lower, upper)
        self.output.delete("0.0", "end")
        self.output.insert(
            "0.0",
            f"\n\tFire Detected!\n\tLOW: {lower}\n\tHIGH: {upper}\n\n"
            f"\tSaved to: '{FIRE_DATA_PATH.relative_to(ROOT_DIR)}'",
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)
    app = Application(master=root)
    app.mainloop()
