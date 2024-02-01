from PIL import Image
from django.core.exceptions import ValidationError
from os.path import splitext

class NoImageError(Exception):
    pass

def validate_icon_image_size(image = None):
    if image is None:
        raise NoImageError("No image provided") 

    # if image:
    with Image.open(image) as img:
        if img.width > 70 or img.height > 70:
            raise ValidationError(
                "The maximum allowed dimensions for the image "
                "are 70x70 - size of image you uploaded: {}".format(img.size)
            )

def validate_image_file_extension(value):
    extension = splitext(value.name)[1]
    valid_extension  = [".jpeg", ".jpg", ".png", ".gif"]
    
    if extension.lower() not in valid_extension:
        raise ValidationError("Unsupported file extension") 