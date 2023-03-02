import urllib.request

SITE_SRC = "https://jnsgr.uk/demo-site"

import logging
from pathlib import Path

LOCAL_CONTENT_PATH = Path("/srv/index.html")


def get_remote_content() -> str:
    logging.info("Downloading site from %s", SITE_SRC)
    with urllib.request.urlopen(SITE_SRC) as response:
        return response.read().decode(encoding="utf-8")


def set_local_content(content: str) -> None:
    if not LOCAL_CONTENT_PATH.is_file():
        LOCAL_CONTENT_PATH.touch()

    LOCAL_CONTENT_PATH.write_text(content, encoding="utf-8")
