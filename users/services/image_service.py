from typing import Any

from ..models import ImageUpload


def create_image_upload(image: Any) -> ImageUpload:
    image = ImageUpload.objects.create(image=image)
    return image