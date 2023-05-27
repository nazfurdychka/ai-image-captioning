from common.common_properties import start_seq_token, end_seq_token
from PIL import Image


def clean_generated_caption(caption):
    return caption.replace(start_seq_token, "").replace(end_seq_token, "").strip()


def is_image(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        return True
    except (IOError, SyntaxError):
        return False
