import shutil

from fastapi import UploadFile


def write_avatar(file_name: str, file: UploadFile):
    with open(file_name, "wb") as bugger:
        shutil.copyfileobj(file.file, bugger)
