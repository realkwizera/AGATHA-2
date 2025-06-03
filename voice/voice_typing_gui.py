import tkinter as tk
from tkinter import messagebox, filedialog
import speech_recognition as sr
import threading

class VoiceTypingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎙️ Voice to Text Typing")
        self.root.geometry("600x400")

        self.text_box = tk.Text(self.root, wrap=tk.WORD, font=("Arial", 14))
        self.text_box.pack(expand=True, fill="both", padx=10, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        self.listen_btn = tk.Button(btn_frame, text="Start Listening", command=self.toggle_listening)
        self.listen_btn.grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Clear", command=self.clear_text).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Copy", command=self.copy_text).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Save", command=self.save_text).grid(row=0, column=3, padx=5)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False

    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_btn.config(text="Stop Listening")
            threading.Thread(target=self.listen).start()
        else:
            self.listening = False
            self.listen_btn.config(text="Start Listening")

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    text = self.recognizer.recognize_google(audio)
                    self.text_box.insert(tk.END, text + " ")
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.text_box.insert(tk.END, "[Unrecognized] ")
                except sr.RequestError:
                    messagebox.showerror("Error", "Speech recognition API error.")
                    break

    def clear_text(self):
        self.text_box.delete("1.0", tk.END)

    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_box.get("1.0", tk.END))
        messagebox.showinfo("Copied", "Text copied to clipboard.")

    def save_text(self):
        content = self.text_box.get("1.0", tk.END)
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Saved to {path}")

    def run(self):
        self.root.mainloop()
