from pathlib import Path

import requests

BOOKS_URL = "https://books.toscrape.com/catalogue/page-1.html"

CACHE_DIR = Path("cache")
CACHE_FILE = CACHE_DIR / "catalogue-page-1.html"


def fetch_page():
    if CACHE_FILE.exists():
        print("CACHE HIT")
        html = CACHE_FILE.read_text(encoding="utf-8")
        print(f"Response size: {len(html)} bytes")
        return html

    print("FETCH")

    headers = {
        "User-Agent": "FlyRankInternship-A5/1.0 (https://github.com/ryan24-rar/be-02-sqlite-crud)"
    }

    response = requests.get(
        BOOKS_URL,
        headers=headers,
        timeout=5,
    )

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    CACHE_DIR.mkdir(exist_ok=True)

    CACHE_FILE.write_text(
        response.text,
        encoding="utf-8",
    )

    print(f"Response size: {len(response.text)} bytes")

    return response.text


if __name__ == "__main__":
    fetch_page()