import os

from fastapi import UploadFile


def delete_file(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def get_extension(filename: str | None):
    return (
        f".{filename.split('.')[-1].lower()}"
        if filename is not None and "." in filename
        else ""
    )


def save_file(file: UploadFile, path: str):
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)

    with open(path, "wb") as f:
        contents = file.file.read()
        f.write(contents)
