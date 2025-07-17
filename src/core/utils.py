from pydantic import HttpUrl


def url_to_str(image_url: HttpUrl) -> str:
    return str(image_url)
