from django.core.exceptions import ValidationError
from PIL import Image
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The maximum image size: 70x70 - size of the image uploaded: {img.size}"
                )


def validate_image_file_extension(image):
    ext = os.path.split(image.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if ext.lower() not in valid_extensions:
        raise ValidationError(
            f"Unsupported file exentions. Supported extensions:{valid_extensions}"
        )
