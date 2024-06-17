# Image Metadata Editor

Image Metadata Editor is a desktop application for viewing and editing image metadata. It supports various image formats and allows you to update metadata such as brand, model, GPS coordinates, and date/time information. The application is built using Python and Tkinter and is easy to use with a modern graphical user interface.

## Features

- **View and Edit Metadata**: Easily view and edit metadata of images, including brand, model, GPS coordinates, and date/time.
- **Batch Processing**: Navigate through a directory of images and update metadata for each image.
- **Modern GUI**: User-friendly and modern graphical user interface built with Tkinter and ttk.
- **Hotkeys**: Quick access to functions with customizable hotkeys.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/tr3xxx/metadata-editor.git
   cd metadata-editor
   ```

2. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```sh
   python main.py
   ```

## Usage

1. **Choose Directory**: On startup, select the directory containing the images you want to edit.
2. **Navigate Images**: Use the "Next" and "Previous" buttons or the corresponding hotkeys to navigate through the images.
3. **Edit Metadata**: Update the metadata fields and click "Save" to apply changes.
4. **Delete Images**: Remove unwanted images from the directory using the "Delete" button.
5. **View Metadata**: Click "Show Metadata" to view detailed metadata in a text file.

### Hotkeys

- **Ctrl+D**: Choose Directory
- **Ctrl+N**: Next Image
- **Ctrl+P**: Previous Image
- **Ctrl+S**: Save Metadata
- **Ctrl+Del**: Delete Image
- **Ctrl+M**: Show Metadata
- **Ctrl+H**: Help

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue.

## Author

Developed by Leon Burghardt

- GitHub: [tr3xxx](https://github.com/tr3xxx)
- LinkedIn: [Leon Burghardt](https://www.linkedin.com/in/leon-burghardt/)

## Acknowledgements

- [Pillow](https://python-pillow.org/): Python Imaging Library (PIL Fork)
- [piexif](https://github.com/hMatoba/piexif): Simplify exif manipulations with Python
