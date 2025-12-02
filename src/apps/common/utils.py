from django.utils.text import slugify
from unidecode import unidecode


def custom_slugify(value: str) -> str:
    return slugify(unidecode(string=value))
