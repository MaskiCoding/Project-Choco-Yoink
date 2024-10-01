import subprocess
import tkinter as tk
from tkinter import messagebox

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

def search_program():
    program_name = entry.get()
    if check_program_exists(program_name):
        result_label.config(text=f"The program '{program_name}' exists in Chocolatey.\nTo install it, use the following command:\nchoco install {program_name}")
    else:
        result_label.config(text=f"The program '{program_name}' does not exist in Chocolatey.")

# Create the main application window
root = tk.Tk()
root.title("Chocolatey Program Checker")

# Create and place the input field and button
tk.Label(root, text="Enter the name of the program:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Check Program", command=search_program).pack(pady=10)

# Label to display the result
result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(pady=10)

# Run the application
root.mainloop()