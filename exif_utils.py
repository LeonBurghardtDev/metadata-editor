from PIL import Image
import piexif

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_bytes = image.info.get("exif")
    exif_dict = piexif.load(exif_bytes) if exif_bytes else {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
    
    brand = exif_dict["0th"].get(piexif.ImageIFD.Make, b'').decode('utf-8') if exif_dict["0th"].get(piexif.ImageIFD.Make) else ''
    model = exif_dict["0th"].get(piexif.ImageIFD.Model, b'').decode('utf-8') if exif_dict["0th"].get(piexif.ImageIFD.Model) else ''
    gps_info = exif_dict.get("GPS", {})

    lat = convert_to_degrees(gps_info.get(piexif.GPSIFD.GPSLatitude))
    lon = convert_to_degrees(gps_info.get(piexif.GPSIFD.GPSLongitude))
    date_time = exif_dict["0th"].get(piexif.ImageIFD.DateTime, b'').decode('utf-8') if exif_dict["0th"].get(piexif.ImageIFD.DateTime) else ''
    gps_date = gps_info.get(piexif.GPSIFD.GPSDateStamp, b'').decode('utf-8') if gps_info.get(piexif.GPSIFD.GPSDateStamp) else ''
    return brand, model, lat, lon, date_time, gps_date

def save_exif_data(image_path, brand, model, lat, lon, date_time):
    image = Image.open(image_path)
    exif_bytes = image.info.get("exif")
    exif_dict = piexif.load(exif_bytes) if exif_bytes else {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}

    exif_dict["0th"][piexif.ImageIFD.Make] = brand.encode('utf-8')
    exif_dict["0th"][piexif.ImageIFD.Model] = model.encode('utf-8')

    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = convert_to_rational(lat)
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = convert_to_rational(lon)
    
    if date_time:
        date_time_bytes = date_time.encode('utf-8')
        exif_dict["0th"][piexif.ImageIFD.DateTime] = date_time_bytes
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = date_time_bytes
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = date_time_bytes
        try:
            date_only = date_time.split()[0]
            exif_dict["GPS"][piexif.GPSIFD.GPSDateStamp] = date_only.encode('utf-8')
        except IndexError:
            print(f"Error: Invalid date_time format: '{date_time}'")

    exif_bytes = piexif.dump(exif_dict)
    image.save(image_path, "jpeg", exif=exif_bytes)

def convert_to_degrees(value):
    if value:
        d0, d1 = value[0]
        m0, m1 = value[1]
        s0, s1 = value[2]
        return d0 / d1 + (m0 / m1) / 60.0 + (s0 / s1) / 3600.0
    return None

def convert_to_rational(value):
    deg = int(value)
    min = int((value - deg) * 60)
    sec = (value - deg - min / 60.0) * 3600.0
    return [(deg, 1), (min, 1), (int(sec * 100), 100)]
