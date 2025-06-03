import cv2
import threading
import tkinter as tk
from PIL import Image, ImageTk

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture-Based Accessibility Tool")
        self.root.geometry("800x600")

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.cap = cv2.VideoCapture(0)
        self.running = True

        self.update_frame()

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            self.root.after(10, self.update_frame)

    def on_close(self):
        self.running = False
        self.cap.release()
        self.root.destroy()

def run_app():
    root = tk.Tk()
    app = GestureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
