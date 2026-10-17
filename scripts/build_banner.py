#!/usr/bin/env python3

from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "assets" / "banner.template.svg"
OUTPUT_PATH = ROOT / "assets" / "banner.svg"


def fetch_avatar(username: str) -> tuple[str, str]:
    url = f"https://github.com/{username}.png?size=332"
    with urlopen(url, timeout=20) as response:
        avatar_bytes = response.read()
        mime = response.headers.get_content_type() or "image/png"

    if not mime or mime == "application/octet-stream":
        mime = mimetypes.guess_type(url)[0] or "image/png"

    return mime, base64.b64encode(avatar_bytes).decode("ascii")


def build_banner(template: str, mime: str, avatar_b64: str) -> str:
    return template.replace("__MIME__", mime).replace("__AVATAR__", avatar_b64)


def main() -> None:
    username = os.environ.get("GITHUB_USER", "").strip() or "RIVALHIDE"

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    mime, avatar_b64 = fetch_avatar(username)
    banner = build_banner(template, mime, avatar_b64)

    OUTPUT_PATH.write_text(banner, encoding="utf-8")
    print(f"Updated {OUTPUT_PATH.name} for @{username}")


if __name__ == "__main__":
    main()
