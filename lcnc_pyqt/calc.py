# import tkinter as tk
# from tkinter import Toplevel

# # Function to create a new window
# def open_window(window_number):
#     new_window = Toplevel(root)
#     new_window.title(f"Window {window_number}")
#     new_window.geometry("300x200")
    
#     label = tk.Label(new_window, text=f"This is Window {window_number}", font=("Arial", 14))
#     label.pack(pady=20)
    
#     # You can add additional widgets to each window as needed
#     close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
#     close_button.pack(pady=10)

# # Create the main window
# root = tk.Tk()
# root.title("Main Window")
# root.geometry("400x300")

# # Create label in the main window
# label = tk.Label(root, text="Click a button to open a new window", font=("Arial", 16))
# label.pack(pady=20)

# # Create buttons to open different windows
# for i in range(1, 6):  # Create 5 buttons
#     button = tk.Button(root, text=f"Open Window {i}", command=lambda i=i: open_window(i), font=("Arial", 12))
#     button.pack(pady=5)

# # Run the main event loop
# root.mainloop()

import os

# Define file path
file_path = "hello.txt"  # You can change this to "example.txt" if you prefer

# 1. Creating and Writing to the File
def create_and_write_file():
    with open(file_path, "w") as file:  # Using the file_path variable here
        file.write("Hello, this is a sample text file.\n")
        file.write("This is the second line.\n")
    print(f"File '{file_path}' created and written successfully.")

# 2. Reading the File
def read_file():
    if os.path.exists(file_path):
        with open(file_path, "r") as file:  # Using the file_path variable here
            content = file.read()
        print("File content:")
        print(content)
    else:
        print(f"File '{file_path}' does not exist.")

# Main Function
if __name__ == "__main__":
    # Create and write to the file
    create_and_write_file()

    # Read and display the file content
    read_file()
