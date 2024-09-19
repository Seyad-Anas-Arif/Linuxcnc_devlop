import tkinter as tk
from tkinter import Toplevel

# Function to create a new window
def open_window(window_number):
    new_window = Toplevel(root)
    new_window.title(f"Window {window_number}")
    new_window.geometry("300x200")
    
    label = tk.Label(new_window, text=f"This is Window {window_number}", font=("Arial", 14))
    label.pack(pady=20)
    
    # You can add additional widgets to each window as needed
    close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
    close_button.pack(pady=10)

# Create the main window
root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")

# Create label in the main window
label = tk.Label(root, text="Click a button to open a new window", font=("Arial", 16))
label.pack(pady=20)

# Create buttons to open different windows
for i in range(1, 6):  # Create 5 buttons
    button = tk.Button(root, text=f"Open Window {i}", command=lambda i=i: open_window(i), font=("Arial", 12))
    button.pack(pady=5)

# Run the main event loop
root.mainloop()
