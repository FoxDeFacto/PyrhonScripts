import tkinter as tk
from tkinter import ttk

# Function to handle button clicks
def button_click(value):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current_text + value)

def clear():
    entry.delete(0, tk.END)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Set up the main application window
root = tk.Tk()
root.title("Jednoduchá kalkulačka")
root.geometry("360x460")
root.resizable(False, False)

# Configure style
style = ttk.Style()
style.configure('TButton', font=('Arial', 14), padding=10)
style.configure('TEntry', font=('Arial', 18))

# Create an entry widget for displaying expressions and results
entry = ttk.Entry(root, font=("Arial", 24))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Define the buttons
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("+", 4, 2), ("=", 4, 3),
    ("C", 5, 0), ("(", 5, 1), (")", 5, 2), ("^", 5, 3)
]

# Create buttons and assign them to the grid
for (text, row, col) in buttons:
    if text == "=":
        button = ttk.Button(root, text=text, command=calculate)
    elif text == "C":
        button = ttk.Button(root, text=text, command=clear)
    elif text == "^":
        button = ttk.Button(root, text=text, command=lambda: button_click("**"))
    else:
        button = ttk.Button(root, text=text, command=lambda t=text: button_click(t))
    
    button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

# Configure grid weights to allow dynamic resizing
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Start the GUI event loop
root.mainloop()
