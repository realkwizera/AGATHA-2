import os
import sys
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import subprocess

def create_icon():
    img = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(img)
    draw.ellipse((10, 10, 54, 54), fill="yellow")
    draw.text((15, 22), "AI", fill="black")
    return img

def run_gesture_app():
    path = os.path.join("gui", "main_overlay.py")
    subprocess.Popen([sys.executable, path])

def run_voice_app():
    path = os.path.join("voice", "main_voice.py")
    subprocess.Popen([sys.executable, path])

def start_tray():
    icon = Icon("AI Tray")
    icon.icon = create_icon()
    icon.menu = Menu(
        MenuItem("Run Gesture App", lambda: threading.Thread(target=run_gesture_app).start()),
        MenuItem("Run Voice Typing", lambda: threading.Thread(target=run_voice_app).start()),
        MenuItem("Exit", lambda: icon.stop())
    )
    icon.run()
