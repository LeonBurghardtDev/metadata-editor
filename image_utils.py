import os
from PIL import Image, ImageTk

def load_images(folder_path):
    return [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg'))]

def load_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((500, 500))
    return ImageTk.PhotoImage(image)
