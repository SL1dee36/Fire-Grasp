import customtkinter
from PIL import Image, ImageTk
import threading
import time
import cv2
import sys
sys.path.append("C:\\Users\\Артём\\Desktop\\Fire-Grasp-main")
from main import FireDetection
from functions.detect_fire import detect_fire
from functions.detect_fire_direction import detect_fire_direction
import pyautogui
import numpy as np
from collections import deque

WIDTH = 1280
HEIGHT = 720

DIRECTIONS_QUEUE_MAXLEN = 25
SEGMENT_SIZE = 20
HEXAGON_SIZE = 96
OUTLINE_TYPE = 'SURFACE AREA' #RECTANGLE, HEXAGON

KERNEL_SIZE = (1, 1)
DILATE_ITERATIONS = 320
ERODE_ITERATIONS = 550

class UI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.show_direction = False
        self.segment_size = SEGMENT_SIZE
        self.hexagon_size = HEXAGON_SIZE
        self.outline_type = OUTLINE_TYPE
        self.kernel_size = KERNEL_SIZE
        self.dilate_iterations = DILATE_ITERATIONS
        self.erode_iterations = ERODE_ITERATIONS
        self.prev_center = {}
        self.directions_queue = deque(maxlen=DIRECTIONS_QUEUE_MAXLEN)

        self.l_h = 5
        self.l_s = 100
        self.l_v = 200
        self.h_h = 26
        self.h_s = 255
        self.h_v = 255

        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.iconbitmap(f"assets\FireGrasp.ico")
        self.title("FIRE.GRASP UI: v1.0")
        self.minsize(WIDTH, HEIGHT)
        self.bind("<<Configure>>", self.current_size)

        self.FDFrame = customtkinter.CTkFrame(self, width=WIDTH // 1.3, height=HEIGHT)
        self.FDFrame.pack(padx=5, pady=5, side='left', fill="both", expand=True)
        self.FDFrame.propagate(0) 

        self.button_S = customtkinter.CTkButton(self.FDFrame, text="START", command=self.run_fire_detection)
        self.button_S.pack(padx=20, pady=20,side='bottom')

        self.canvas = customtkinter.CTkCanvas(self.FDFrame, width=WIDTH // 1.3, height=HEIGHT, bd=0,bg="#2B2B2B", highlightthickness=0) 
        self.canvas.pack(fill="both", expand=True)
        self.canvas.propagate(0) 

        self.SettingsFrame = customtkinter.CTkFrame(self, width=(WIDTH - WIDTH // 1.3), height=HEIGHT, corner_radius=0)
        self.SettingsFrame.pack(side='left', fill="y")

        self.titleFrame = customtkinter.CTkFrame(self.SettingsFrame,height=48,width=180, corner_radius=8)
        self.titleFrame.pack(side='top',padx=5,pady=5)
        self.titleFrame.propagate(0)
        
        self.title = customtkinter.CTkLabel(self.titleFrame,text='SETTINGS',font=('consolas',24),anchor='center')
        self.title.pack(padx=5,pady=10)

        self.RESET_btn = customtkinter.CTkButton(self.SettingsFrame, text="Default detector", command=self.reset_tolerance)
        self.RESET_btn.pack(padx=20, pady=10)

        self.outlineTitle = customtkinter.CTkLabel(self.SettingsFrame,text='Select outline type',font=('consolas',12))
        self.outlineTitle.pack()

        self.outline_type_temp = customtkinter.StringVar(value="SURFACE AREA")
        self.outlineSelect = customtkinter.CTkOptionMenu(self.SettingsFrame,values=["SURFACE AREA", "RECTANGLE", "HEXAGON"],command=self.outlineSelect_callback,variable=self.outline_type_temp)
        self.outlineSelect.pack()

        self.toleranceTitle = customtkinter.CTkLabel(self.SettingsFrame,text='Tolerance',font=('consolas',12))
        self.toleranceTitle.pack()

        self.l_h_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=0, to=255, command=lambda value: self.update_value("l_h", value))
        self.l_h_slider.set(self.l_h)
        self.l_h_slider.pack(pady=5)
        self.l_h_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"L - H: {self.l_h}")
        self.l_h_label.pack()

        self.l_s_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=0, to=255, command=lambda value: self.update_value("l_s", value))
        self.l_s_slider.set(self.l_s)
        self.l_s_slider.pack(pady=5)
        self.l_s_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"L - S: {self.l_s}")
        self.l_s_label.pack()

        self.l_v_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=0, to=255, command=lambda value: self.update_value("l_v", value))
        self.l_v_slider.set(self.l_v)
        self.l_v_slider.pack(pady=5)
        self.l_v_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"L - V: {self.l_v}")
        self.l_v_label.pack()

        self.h_h_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=0, to=255, command=lambda value: self.update_value("h_h", value))
        self.h_h_slider.set(self.h_h)
        self.h_h_slider.pack(pady=5)
        self.h_h_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"H - H: {self.h_h}")
        self.h_h_label.pack()

        self.h_s_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=0, to=255, command=lambda value: self.update_value("h_s", value))
        self.h_s_slider.set(self.h_s)
        self.h_s_slider.pack(pady=5)
        self.h_s_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"H - S: {self.h_s}")
        self.h_s_label.pack()

        self.h_v_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=0, to=255, command=lambda value: self.update_value("h_v", value))
        self.h_v_slider.set(self.h_v)
        self.h_v_slider.pack(pady=5)
        self.h_v_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"H - V: {self.h_v}")
        self.h_v_label.pack()

        self.segmentation_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"\nSegment Size: {self.segment_size}")
        self.segmentation_label.pack()

        self.segmentation_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=2, to=200, command=lambda value: self.update_value("segment_size", value))
        self.segmentation_slider.set(self.segment_size)
        self.segmentation_slider.pack(pady=5)

        self.dilate_iterations_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"\nDilate iterations: {self.dilate_iterations}")
        self.dilate_iterations_label.pack()

        self.dilate_iterations_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=2, to=2048, command=lambda value: self.update_value("dilate_iterations", value))
        self.dilate_iterations_slider.set(self.dilate_iterations)
        self.dilate_iterations_slider.pack(pady=5)

        self.erode_iterations_label = customtkinter.CTkLabel(self.SettingsFrame, text=f"\nErode iterations: {self.erode_iterations}")
        self.erode_iterations_label.pack()

        self.erode_iterations_slider = customtkinter.CTkSlider(self.SettingsFrame, from_=2, to=2048, command=lambda value: self.update_value("erode_iterations", value))
        self.erode_iterations_slider.set(self.erode_iterations)
        self.erode_iterations_slider.pack(pady=5)

    def reset_tolerance(self):
        self.l_h = 5
        self.l_s = 100
        self.l_v = 200
        self.h_h = 28
        self.h_s = 255
        self.h_v = 255

        self.segment_size = SEGMENT_SIZE
        self.dilate_iterations = DILATE_ITERATIONS
        self.erode_iterations = ERODE_ITERATIONS

        self.l_h_slider.set(self.l_h)
        self.l_s_slider.set(self.l_s)
        self.l_v_slider.set(self.l_v)
        self.h_h_slider.set(self.h_h)
        self.h_s_slider.set(self.h_s)
        self.h_v_slider.set(self.h_v)

        self.segmentation_slider.set(self.segment_size)
        self.dilate_iterations_slider.set(self.dilate_iterations)
        self.erode_iterations_slider.set(self.erode_iterations)

        self.l_h_label.configure(text=f"L - H: {self.l_h}")
        self.l_s_label.configure(text=f"L - S: {self.l_s}")
        self.l_v_label.configure(text=f"L - V: {self.l_v}")
        self.h_h_label.configure(text=f"H - H: {self.h_h}")
        self.h_s_label.configure(text=f"H - S: {self.h_s}")
        self.h_v_label.configure(text=f"H - V: {self.h_v}")

        self.segmentation_label.configure(text=f"\nSegment Size: {self.segment_size}")
        self.dilate_iterations_label.configure(text=f"\nDilate iterations: {self.dilate_iterations}")
        self.erode_iterations_label.configure(text=f"\nErode iterations: {self.erode_iterations}")

    def update_value(self, variable_name, value):
        setattr(self, variable_name, int(value))
        if variable_name == "l_h":
            self.l_h_label.configure(text=f"L - H: {self.l_h}")
        elif variable_name == "l_s":
            self.l_s_label.configure(text=f"L - S: {self.l_s}")
        elif variable_name == "l_v":
            self.l_v_label.configure(text=f"L - V: {self.l_v}")
        elif variable_name == "h_h":
            self.h_h_label.configure(text=f"H - H: {self.h_h}")
        elif variable_name == "h_s":
            self.h_s_label.configure(text=f"H - S: {self.h_s}")
        elif variable_name == "h_v":
            self.h_v_label.configure(text=f"H - V: {self.h_v}")
        elif variable_name == "segment_size":
            self.segmentation_label.configure(text=f"\nSegment Size: {self.segment_size}")
        elif variable_name == "dilate_iterations":
            self.dilate_iterations_label.configure(text=f"\nDilate iterations: {self.dilate_iterations}")
        elif variable_name == "erode_iterations":
            self.erode_iterations_label.configure(text=f"\nErode iterations: {self.erode_iterations}")

    def outlineSelect_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

        self.outline_type = choice
    
    def run_fire_detection(self):
        self.button_S.forget()
        while True:
            curr_frame = pyautogui.screenshot()
            curr_frame = np.array(curr_frame)
            curr_frame = curr_frame[:, :, ::-1].copy()

            curr_frame, contours = detect_fire(curr_frame, False, self.outline_type, self.segment_size, 
                                               (self.l_h, self.l_s, self.l_v), (self.h_h, self.h_s, self.h_v), self.dilate_iterations, self.erode_iterations)
            if self.show_direction:
                curr_frame = detect_fire_direction(curr_frame, contours, self.prev_center)

            if curr_frame is not None:

                height, width = curr_frame.shape[:2]
                aspect_ratio = width / height
                if aspect_ratio > 16/9:

                    new_width = int(height * 16/9)
                    curr_frame = curr_frame[:, (width - new_width) // 2:(width + new_width) // 2]
                else:

                    new_height = int(width * 9/16)
                    curr_frame = curr_frame[(height - new_height) // 2:(height + new_height) // 2, :]

                canvas_width = int(self.FDFrame.winfo_width())  # Получаем ширину canvas
                curr_frame = cv2.resize(curr_frame, (canvas_width, int(canvas_width * 9 / 16))) 

                curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(curr_frame)

                self.canvas.delete("all") 
                photo = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, anchor="nw", image=photo)
                self.canvas.imgtk = photo  

                self.canvas.update() 

    def current_size(self, event):
        new_width = event.width
        new_height = event.height

        self.FDFrame.pack_configure(width=new_width // 1.3, height=new_height)
        self.canvas.config(width=new_width // 1.3, height=new_height)

app = UI()
app.mainloop()