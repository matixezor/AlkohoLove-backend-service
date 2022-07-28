import os


def image_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0, os.SEEK_SET)
    return size


def get_suggestion_image_name(alcohol_name: str, suggestion_id: str):
    return alcohol_name.lower().replace(' ', '_') + '_' + suggestion_id
