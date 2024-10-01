import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time
from icon_fetcher import fetch_program_icon

def create_gui():
    def check_program_exists(program_name):
        try:
            result = subprocess.run(['choco', 'search', program_name], capture_output=True, text=True)
            if program_name.lower() in result.stdout.lower():
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def search_program(event=None):
        program_name = entry.get()
        result_label.config(text="Searching...")
        search_button.pack_forget()
        loading_thread = threading.Thread(target=show_loading_animation)
        loading_thread.start()
        
        def search():
            if check_program_exists(program_name):
                result = f"The program '{program_name}' exists in Chocolatey.\nTo install it, use the following command:\nchoco install {program_name}"
                icon_image = fetch_program_icon(program_name)
                if icon_image:
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    icon_label.config(image=icon_photo)
                    icon_label.image = icon_photo
                    print("Icon displayed successfully")
                else:
                    icon_label.config(image='')
                    print("No icon to display")
            else:
                result = f"The program '{program_name}' does not exist in Chocolatey."
                icon_label.config(image='')
            result_label.config(text=result)
            global stop_loading
            stop_loading = True
            search_button.pack(pady=10)

        search_thread = threading.Thread(target=search)
        search_thread.start()

    def show_loading_animation():
        global stop_loading
        stop_loading = False
        animation = ["|", "/", "-", "\\"]
        idx = 0
        while not stop_loading:
            result_label.config(text=f"Searching... {animation[idx % len(animation)]}")
            idx += 1
            time.sleep(0.1)

    root = tk.Tk()
    root.title("Chocolatey Program Checker")

    tk.Label(root, text="Enter the name of the program:").pack(pady=5)
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)
    entry.bind('<Return>', search_program)

    search_button = tk.Button(root, text="Check Program", command=search_program)
    search_button.pack(pady=10)

    result_label = tk.Label(root, text="", wraplength=400)
    result_label.pack(pady=10)

    icon_label = tk.Label(root)
    icon_label.pack(pady=10)

    root.mainloop()
