import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the keys from environment variables
PUBLIC_KEY = os.getenv("LOGO_DEV_PUBLIC_KEY")
SECRET_KEY = os.getenv("LOGO_DEV_SECRET_KEY")

def check_program_exists(program_name):
    try:
        # Run the choco search command
        result = subprocess.run(['choco', 'search', program_name], capture_output=True, text=True)
        
        # Check if the program exists in the search results
        if program_name.lower() in result.stdout.lower():
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def fetch_program_icon(program_name):
    try:
        # Fetch the Chocolatey package page
        url = f"https://community.chocolatey.org/packages/{program_name}"
        print(f"Fetching icon from URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the icon URL in the page
            icon_tag = soup.find('img', class_='package-icon')
            if icon_tag and 'src' in icon_tag.attrs:
                icon_url = icon_tag['src']
                print(f"Icon URL: {icon_url}")
                icon_response = requests.get(icon_url)
                if icon_response.status_code == 200:
                    return Image.open(BytesIO(icon_response.content))
        print(f"Failed to fetch icon from Chocolatey page, status code: {response.status_code}")
        # Fallback to default icon
        return Image.open("default.png")
    except Exception as e:
        print(f"An error occurred while fetching the icon: {e}")
        return Image.open("default.png")

def search_program(event=None):
    program_name = entry.get()
    result_label.config(text="Searching...")
    search_button.pack_forget()  # Hide the search button
    loading_thread = threading.Thread(target=show_loading_animation)
    loading_thread.start()
    
    def search():
        if check_program_exists(program_name):
            result = f"The program '{program_name}' exists in Chocolatey.\nTo install it, use the following command:\nchoco install {program_name}"
            icon_image = fetch_program_icon(program_name)
            if icon_image:
                icon_photo = ImageTk.PhotoImage(icon_image)
                icon_label.config(image=icon_photo)
                icon_label.image = icon_photo  # Keep a reference to avoid garbage collection
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
        search_button.pack(pady=10)  # Show the search button again

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

# Create the main application window
root = tk.Tk()
root.title("Chocolatey Program Checker")

# Create and place the input field and button
tk.Label(root, text="Enter the name of the program:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)
entry.bind('<Return>', search_program)  # Bind the Enter key to the search_program function

search_button = tk.Button(root, text="Check Program", command=search_program)
search_button.pack(pady=10)

# Label to display the result
result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(pady=10)

# Label to display the icon
icon_label = tk.Label(root)
icon_label.pack(pady=10)

# Run the application
root.mainloop()