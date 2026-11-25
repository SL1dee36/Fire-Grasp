from collections import deque
from pathlib import Path
import sys
import threading

import customtkinter
import cv2
from PIL import Image, ImageTk

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from functions.detect_fire import DILATE_ITERATIONS, ERODE_ITERATIONS, KERNEL_SIZE, detect_fire
from functions.detect_fire_direction import detect_fire_direction
from functions.utils import capture_screen, load_fire_bounds

WIDTH = 1280
HEIGHT = 720

DIRECTIONS_QUEUE_MAXLEN = 25
SEGMENT_SIZE = 20
HEXAGON_SIZE = 96
OUTLINE_TYPE = "SURFACE AREA"


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

        lower, upper = load_fire_bounds()
        self.l_h, self.l_s, self.l_v = lower
        self.h_h, self.h_s, self.h_v = upper

        self._stop_event = threading.Event()
        self._worker_thread = None
        self._frame_lock = threading.Lock()
        self._latest_image = None
        self._photo = None

        self.geometry(f"{WIDTH}x{HEIGHT}")
        icon_path = ROOT_DIR / "assets" / "FireGrasp.ico"
        if icon_path.is_file():
            self.iconbitmap(str(icon_path))
        self.title("FIRE.GRASP UI: v1.0")
        self.minsize(WIDTH, HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.FDFrame = customtkinter.CTkFrame(self, width=int(WIDTH // 1.3), height=HEIGHT)
        self.FDFrame.pack(padx=5, pady=5, side="left", fill="both", expand=True)
        self.FDFrame.pack_propagate(False)

        self.button_S = customtkinter.CTkButton(self.FDFrame, text="START", command=self.toggle_detection)
        self.button_S.pack(padx=20, pady=12, side="bottom")

        self.canvas = customtkinter.CTkCanvas(
            self.FDFrame,
            width=int(WIDTH // 1.3),
            height=HEIGHT,
            bd=0,
            bg="#2B2B2B",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.SettingsFrame = customtkinter.CTkScrollableFrame(
            self,
            width=WIDTH - int(WIDTH // 1.3),
            height=HEIGHT,
            corner_radius=0,
        )
        self.SettingsFrame.pack(side="left", fill="y")

        self.titleFrame = customtkinter.CTkFrame(self.SettingsFrame, height=48, width=180, corner_radius=8)
        self.titleFrame.pack(side="top", padx=5, pady=5)
        self.titleFrame.pack_propagate(False)

        self.title_label = customtkinter.CTkLabel(
            self.titleFrame, text="SETTINGS", font=("consolas", 24), anchor="center"
        )
        self.title_label.pack(padx=5, pady=10)

        self.RESET_btn = customtkinter.CTkButton(
            self.SettingsFrame, text="Default detector", command=self.reset_tolerance
        )
        self.RESET_btn.pack(padx=20, pady=10)

        self.direction_switch = customtkinter.CTkSwitch(
            self.SettingsFrame, text="Show direction", command=self.toggle_direction
        )
        self.direction_switch.pack(pady=6)

        self.outlineTitle = customtkinter.CTkLabel(
            self.SettingsFrame, text="Select outline type", font=("consolas", 12)
        )
        self.outlineTitle.pack()

        self.outline_type_temp = customtkinter.StringVar(value=self.outline_type)
        self.outlineSelect = customtkinter.CTkOptionMenu(
            self.SettingsFrame,
            values=["SURFACE AREA", "RECTANGLE", "HEXAGON"],
            command=self.outline_select_callback,
            variable=self.outline_type_temp,
        )
        self.outlineSelect.pack(pady=(0, 8))

        self.toleranceTitle = customtkinter.CTkLabel(self.SettingsFrame, text="Tolerance", font=("consolas", 12))
        self.toleranceTitle.pack()

        self._sliders = {}
        slider_specs = [
            ("l_h", "L - H", 0, 255, self.l_h),
            ("l_s", "L - S", 0, 255, self.l_s),
            ("l_v", "L - V", 0, 255, self.l_v),
            ("h_h", "H - H", 0, 255, self.h_h),
            ("h_s", "H - S", 0, 255, self.h_s),
            ("h_v", "H - V", 0, 255, self.h_v),
            ("hexagon_size", "Hexagon Size", 10, 200, self.hexagon_size),
            ("dilate_iterations", "Dilate iterations", 0, 20, self.dilate_iterations),
            ("erode_iterations", "Erode iterations", 0, 20, self.erode_iterations),
        ]

        for attr, title, min_v, max_v, initial in slider_specs:
            slider = customtkinter.CTkSlider(
                self.SettingsFrame,
                from_=min_v,
                to=max_v,
                command=lambda value, a=attr, t=title: self.update_value(a, t, value),
            )
            slider.set(initial)
            slider.pack(pady=4)
            label = customtkinter.CTkLabel(self.SettingsFrame, text=f"{title}: {initial}")
            label.pack()
            self._sliders[attr] = (slider, label, title)

    def toggle_direction(self):
        self.show_direction = bool(self.direction_switch.get())

    def reset_tolerance(self):
        defaults = {
            "l_h": 5,
            "l_s": 100,
            "l_v": 200,
            "h_h": 28,
            "h_s": 255,
            "h_v": 255,
            "hexagon_size": HEXAGON_SIZE,
            "dilate_iterations": DILATE_ITERATIONS,
            "erode_iterations": ERODE_ITERATIONS,
        }
        for attr, val in defaults.items():
            setattr(self, attr, val)
            slider, label, title = self._sliders[attr]
            slider.set(val)
            label.configure(text=f"{title}: {val}")

    def update_value(self, attr, title, value):
        int_val = int(value)
        setattr(self, attr, int_val)
        _, label, _ = self._sliders[attr]
        label.configure(text=f"{title}: {int_val}")

    def outline_select_callback(self, choice):
        self.outline_type = choice

    def toggle_detection(self):
        if self._worker_thread is not None and self._worker_thread.is_alive():
            self._stop_event.set()
            self.button_S.configure(text="START")
            return

        self._stop_event.clear()
        self.button_S.configure(text="STOP")
        self._worker_thread = threading.Thread(target=self._detection_worker, daemon=True)
        self._worker_thread.start()
        self.after(15, self._render_latest_frame)

    def _detection_worker(self):
        while not self._stop_event.is_set():
            curr_frame = capture_screen()
            curr_frame, contours = detect_fire(
                curr_frame,
                False,
                self.outline_type,
                self.hexagon_size,
                (self.l_h, self.l_s, self.l_v),
                (self.h_h, self.h_s, self.h_v),
                self.dilate_iterations,
                self.erode_iterations,
                kernel_size=self.kernel_size,
            )
            if self.show_direction:
                curr_frame = detect_fire_direction(curr_frame, contours, self.prev_center)

            height, width = curr_frame.shape[:2]
            aspect_ratio = width / height
            if aspect_ratio > 16 / 9:
                new_width = int(height * 16 / 9)
                curr_frame = curr_frame[:, (width - new_width) // 2 : (width + new_width) // 2]
            else:
                new_height = int(width * 9 / 16)
                curr_frame = curr_frame[(height - new_height) // 2 : (height + new_height) // 2, :]

            canvas_width = max(320, self.canvas.winfo_width())
            canvas_height = max(180, int(canvas_width * 9 / 16))
            curr_frame = cv2.resize(curr_frame, (canvas_width, canvas_height))
            rgb_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)

            with self._frame_lock:
                self._latest_image = img

    def _render_latest_frame(self):
        if self._stop_event.is_set():
            return

        img = None
        with self._frame_lock:
            if self._latest_image is not None:
                img = self._latest_image
                self._latest_image = None

        if img is not None:
            self._photo = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self._photo)

        self.after(15, self._render_latest_frame)

    def on_close(self):
        self._stop_event.set()
        self.destroy()


if __name__ == "__main__":
    app = UI()
    app.mainloop()
