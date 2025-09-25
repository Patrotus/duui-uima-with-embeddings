import base64
from io import BytesIO
from PIL import Image

from app.constants import STATIC_IMAGE_FORMAT, STATIC_ENCODING


def image_to_base64_url(pil_image: Image.Image) -> str:
    with BytesIO() as bio:
        pil_image.save(bio, format=STATIC_IMAGE_FORMAT)
        return base64.b64encode(bio.getvalue()).decode(STATIC_ENCODING)


def base64_url_to_image(base64_url: str) -> Image.Image:
    img_data = base64.b64decode(base64_url)
    return Image.open(BytesIO(img_data))
