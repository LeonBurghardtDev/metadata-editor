import tkinter as tk
from tkinter import filedialog
from gui import create_main_window
from image_utils import load_images

def main():
    root = tk.Tk()
    root.withdraw()  

    MessageBox = tk.messagebox.askquestion('Image Metadata Editor', 'Please select the folder containing the metadata images to be edited', icon='info')
    if MessageBox == 'no':
        return
    folder_path = filedialog.askdirectory(title="Select Image Directory")
    if not folder_path:
        return  

    root.deiconify() 
    root.title("Image Metadata Editor")
    root.configure(bg='white')
    root.resizable(False, False)
    
    icon_path = 'Assets/Icon.ico'
    root.iconbitmap(icon_path)

    images = load_images(folder_path)
    current_image_index = 0

    create_main_window(root, images, folder_path, current_image_index)
    root.mainloop()

if __name__ == "__main__":
    main()
