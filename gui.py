import os
import tempfile
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ExifTags
from datetime import datetime
from exif_utils import get_exif_data, save_exif_data
from image_utils import load_image, load_images

def create_main_window(root, images, folder_path, current_image_index):
    def update_image():
        nonlocal current_image_index
        if current_image_index < 0 or current_image_index >= len(images):
            return

        image_path = os.path.join(folder_path, images[current_image_index])
        img = load_image(image_path)
        brand, model, lat, lon, date_time, gps_date = get_exif_data(image_path)

        image_label.config(image=img)
        image_label.image = img
        filename_var.set(os.path.basename(image_path))
        brand_var.set(brand)
        model_var.set(model)
        lat_var.set(lat if lat is not None else '')
        lon_var.set(lon if lon is not None else '')

        if date_time:
            try:
                dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                dt = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S')
            date_var.set(dt.strftime('%Y-%m-%d'))
            time_var.set(dt.strftime('%H:%M:%S'))
        else:
            date_var.set('')
            time_var.set('')

    def save_metadata():
        nonlocal current_image_index
        if current_image_index < 0 or current_image_index >= len(images):
            return

        image_path = os.path.join(folder_path, images[current_image_index])
        new_filename = filename_var.get()
        new_image_path = os.path.join(folder_path, new_filename)
        
        brand = brand_var.get()
        model = model_var.get()
        lat = float(lat_var.get()) if lat_var.get() else 0.0
        lon = float(lon_var.get()) if lon_var.get() else 0.0
        date_time = f"{date_var.get()} {time_var.get()}"

        save_exif_data(image_path, brand, model, lat, lon, date_time)

        if new_filename != os.path.basename(image_path):
            os.rename(image_path, new_image_path)
            images[current_image_index] = new_filename

        messagebox.showinfo("Info", "Metadata updated successfully.")

    def delete_image():
        nonlocal current_image_index
        if current_image_index < 0 or current_image_index >= len(images):
            return

        image_path = os.path.join(folder_path, images[current_image_index])
        os.remove(image_path)
        del images[current_image_index]

        if current_image_index >= len(images):
            current_image_index = len(images) - 1

        if images:
            update_image()
        else:
            image_label.config(image='')
            filename_var.set('')
            brand_var.set('')
            model_var.set('')
            lat_var.set('')
            lon_var.set('')
            date_var.set('')
            time_var.set('')

    def show_metadata():
        if current_image_index < 0 or current_image_index >= len(images):
            return

        image_path = os.path.join(folder_path, images[current_image_index])
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            metadata_str = ""

            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    metadata_str += f"{tag:25}: {value}\n"
            else:
                metadata_str = "No EXIF metadata found."

            temp_dir = tempfile.gettempdir()
            metadata_file = os.path.join(temp_dir, "metadata.txt")
            with open(metadata_file, 'w', encoding='utf-8') as file:
                file.write(metadata_str)

            os.system(f'notepad.exe {metadata_file}')
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    def next_image():
        nonlocal current_image_index
        if current_image_index < len(images) - 1:
            current_image_index += 1
            update_image()

    def prev_image():
        nonlocal current_image_index
        if current_image_index > 0:
            current_image_index -= 1
            update_image()

    def choose_directory():
        nonlocal folder_path, images, current_image_index
        new_folder_path = filedialog.askdirectory(title="Select Image Directory")
        if new_folder_path:
            folder_path = new_folder_path
            images = load_images(folder_path)
            current_image_index = 0
            if images:
                update_image()
            else:
                image_label.config(image='')
                filename_var.set('')
                brand_var.set('')
                model_var.set('')
                lat_var.set('')
                lon_var.set('')
                date_var.set('')
                time_var.set('')
                messagebox.showinfo("Info", "No images found in the selected directory.")

    def show_help():
        messagebox.showinfo("Info", "Image Metadata Editor\n\nDeveloped by Leon Burghardt\nhttps://github.com/tr3xxx/metadata-editor\nLicensed under the MIT License\nVersion 1.0")

    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    menu_bar = tk.Menu(root, bg='white', fg='black')
    
    choose_directory_menu = tk.Menu(menu_bar, tearoff=0, bg='white', fg='black')
    choose_directory_menu.add_command(label="Choose Directory", command=choose_directory, accelerator="Ctrl+D")
    menu_bar.add_cascade(label="Directory", menu=choose_directory_menu)

    file_menu = tk.Menu(menu_bar, tearoff=0, bg='white', fg='black')
    file_menu.add_command(label="Next", command=next_image, accelerator="Ctrl+N")
    file_menu.add_command(label="Previous", command=prev_image, accelerator="Ctrl+P")
    file_menu.add_separator()
    file_menu.add_command(label="Save", command=save_metadata, accelerator="Ctrl+S")
    file_menu.add_command(label="Delete", command=delete_image, accelerator="Ctrl+Del")
    file_menu.add_command(label="Show Metadata", command=show_metadata, accelerator="Ctrl+M")
    menu_bar.add_cascade(label="File", menu=file_menu)

    help_menu = tk.Menu(menu_bar, tearoff=0, bg='white', fg='black')
    help_menu.add_command(label="Info", command=show_help, accelerator="Ctrl+H")
    menu_bar.add_cascade(label="Info", menu=help_menu)

    root.config(menu=menu_bar)

    root.bind_all("<Control-d>", lambda event: choose_directory())
    root.bind_all("<Control-n>", lambda event: next_image())
    root.bind_all("<Control-p>", lambda event: prev_image())
    root.bind_all("<Control-s>", lambda event: save_metadata())
    root.bind_all("<Control-Delete>", lambda event: delete_image())
    root.bind_all("<Control-m>", lambda event: show_metadata())
    root.bind_all("<Control-h>", lambda event: show_help())

    image_frame = tk.Frame(main_frame, bg='white')
    image_frame.grid(row=0, column=0, rowspan=7, padx=10, pady=10)

    global image_label
    image_label = tk.Label(image_frame, bg='white')
    image_label.pack()

    fields_frame = tk.Frame(main_frame, bg='white')
    fields_frame.grid(row=0, column=1, sticky='n')

    filename_label = tk.Label(fields_frame, text="Filename:", bg='white')
    filename_label.grid(row=0, column=0, sticky='e')
    global filename_var
    filename_var = tk.StringVar()
    filename_entry = tk.Entry(fields_frame, textvariable=filename_var, bg='white')
    filename_entry.grid(row=0, column=1)

    brand_label = tk.Label(fields_frame, text="Brand:", bg='white')
    brand_label.grid(row=1, column=0, sticky='e')
    global brand_var
    brand_var = tk.StringVar()
    brand_entry = tk.Entry(fields_frame, textvariable=brand_var, bg='white')
    brand_entry.grid(row=1, column=1)

    model_label = tk.Label(fields_frame, text="Model:", bg='white')
    model_label.grid(row=2, column=0, sticky='e')
    global model_var
    model_var = tk.StringVar()
    model_entry = tk.Entry(fields_frame, textvariable=model_var, bg='white')
    model_entry.grid(row=2, column=1)

    lat_label = tk.Label(fields_frame, text="Latitude:", bg='white')
    lat_label.grid(row=3, column=0, sticky='e')
    global lat_var
    lat_var = tk.StringVar()
    lat_entry = tk.Entry(fields_frame, textvariable=lat_var, bg='white')
    lat_entry.grid(row=3, column=1)

    lon_label = tk.Label(fields_frame, text="Longitude:", bg='white')
    lon_label.grid(row=4, column=0, sticky='e')
    global lon_var
    lon_var = tk.StringVar()
    lon_entry = tk.Entry(fields_frame, textvariable=lon_var, bg='white')
    lon_entry.grid(row=4, column=1)

    date_label = tk.Label(fields_frame, text="Date:", bg='white')
    date_label.grid(row=5, column=0, sticky='e')
    global date_var
    date_var = tk.StringVar()
    date_entry = tk.Entry(fields_frame, textvariable=date_var, bg='white')
    date_entry.grid(row=5, column=1)

    time_label = tk.Label(fields_frame, text="Time:", bg='white')
    time_label.grid(row=6, column=0, sticky='e')
    global time_var
    time_var = tk.StringVar()
    time_entry = tk.Entry(fields_frame, textvariable=time_var, bg='white')
    time_entry.grid(row=6, column=1)

    buttons_frame = tk.Frame(main_frame, bg='white')
    buttons_frame.grid(row=7, column=0, columnspan=2, pady=10)

    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")

    prev_button = ttk.Button(buttons_frame, text="Previous", command=prev_image, style="TButton")
    prev_button.grid(row=0, column=0, padx=5)

    next_button = ttk.Button(buttons_frame, text="Next", command=next_image, style="TButton")
    next_button.grid(row=0, column=1, padx=5)

    save_button = ttk.Button(buttons_frame, text="Save", command=save_metadata, style="TButton")
    save_button.grid(row=0, column=2, padx=5)

    delete_button = ttk.Button(buttons_frame, text="Delete", command=delete_image, style="TButton")
    delete_button.grid(row=0, column=3, padx=5)

    show_metadata_button = ttk.Button(buttons_frame, text="Show Metadata", command=show_metadata, style="TButton")
    show_metadata_button.grid(row=0, column=4, padx=5)

    if images:
        update_image()
