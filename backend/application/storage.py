from flask import Blueprint, send_file
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os
from supabase import create_client


bp = Blueprint("storage", __name__)


def drive():
    sb = create_client(os.environ["STORE_URI"], os.environ["STORE_KEY"])
    return sb.storage.from_('portfolio.website')


def storage(method, x, thumbnail=False, path=""):
    if method == "save":
        photo = Image.open(x).convert('RGBA')
        white = Image.new('RGBA', photo.size, (255, 255, 255))
        photo = Image.alpha_composite(white, photo).convert('RGB')

        file_io = BytesIO()
        photo.save(file_io, format="JPEG")
        file_io.seek(0)

        name = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
        drive().upload(
            f"{path}{name}",
            file_io.getvalue(),
            {'content-type': 'image/jpeg'}
        )

        return name

    elif method == "get":
        photo = drive().download(f"{path}{x}")
        photo = Image.open(BytesIO(photo))

        if thumbnail:
            size = int(thumbnail)
            photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)

        file_io = BytesIO()
        photo.save(file_io, format="JPEG")
        file_io.seek(0)

        return file_io

    elif method == "delete":
        return drive().remove([f"{path}{x}"])


@bp.get("/file/<filename>")
@bp.get("/file/<filename>/<thumbnail>")
def get_photo(filename, thumbnail=False):
    file = storage("get", filename, thumbnail=thumbnail)
    return send_file(file, mimetype="image/jpg")
