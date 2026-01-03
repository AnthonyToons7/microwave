import os
from PIL import (
    Image,
    ImageTk
)

def create_image_model(path):
    img_path = os.path.join(os.path.dirname(__file__), path)
    img = Image.open(img_path)
    img = img.resize((300, 220), Image.LANCZOS)
    microwave_img = ImageTk.PhotoImage(img)

    return microwave_img