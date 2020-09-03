# python standard lib
import base64
import io
import re
import secrets

from django.core.files.base import ContentFile

# django and pillow lib
from PIL import Image


def camelcase_to_snake(value):
    value = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", value)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", value).lower()


def snake_to_camelcase(value):
    def camelcase():
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(c.next()(x) if x else "_" for x in value.split("_"))


def get_image_from_data_url(data_url, resize=True, base_width=600):

    # getting the file format and the necessary dataURl for the file
    _format, _dataurl = data_url.split(";base64,")
    # file name and extension
    _filename, _extension = secrets.token_hex(20), _format.split("/")[-1]
    print("FILENAME", _filename, _extension)

    # generating the contents of the file
    file = ContentFile(base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

    # resizing the image, reducing quality and size
    if resize:

        # opening the file with the pillow
        image = Image.open(file)
        # using BytesIO to rewrite the new content without using the filesystem
        image_io = io.BytesIO()

        # resize
        w_percent = base_width / float(image.size[0])
        h_size = int((float(image.size[1]) * float(w_percent)))
        image = image.resize((base_width, h_size), Image.ANTIALIAS)

        # save resized image
        image.save(image_io, format=_extension)

        # generating the content of the new image
        file = ContentFile(image_io.getvalue(), name=f"{_filename}.{_extension}")

    # file and filename
    return file, (_filename, _extension)
