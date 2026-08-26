print("RUNNING NEW VERSION")

from pathlib import Path
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

BOOKS_URL = "https://books.toscrape.com/catalogue/page-1.html"

CACHE_DIR = Path("cache")
def cache_file(url):
    filename = url.split("/")[-1]

    if filename == "":
        filename = "index"

    return CACHE_DIR / f"{filename}.html"


def fetch_page(url):

    cache= cache_file(url)

    if cache.exists():
        print("CACHE HIT")
        html = cache.read_text(encoding="utf-8")
        print(f"Response size: {len(html)} bytes")
        return html

    print("FETCH")

    headers = {
        "User-Agent": "FlyRankInternship-A5/1.0 (https://github.com/ryan24-rar/be-02-sqlite-crud)"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=5,
    )

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    CACHE_DIR.mkdir(exist_ok=True)

    cache.write_text(
        response.text,
        encoding="utf-8",
    )

    print(f"Response size: {len(response.text)} bytes")

    return response.text

def parse_catalogue(html, current_url):
    soup = BeautifulSoup(html, "html.parser")

    book_links = []

    for article in soup.select("article.product_pod h3 a"):
        href = article["href"]
        absolute_url = urljoin(current_url, href)
        book_links.append(absolute_url)

    next_page = None

    next_link = soup.select_one("li.next a")

    if next_link:
        next_page = urljoin(current_url, next_link["href"])

    return book_links, next_page




if __name__ == "__main__":
    current_url = BOOKS_URL

    all_books = []

    catalogue_pages = 0

    while current_url and catalogue_pages < 3:

        html = fetch_page(current_url)

        books, current_url = parse_catalogue(html, current_url)

        all_books.extend(books)

        catalogue_pages += 1

        if current_url:
            time.sleep(0.5)

    unique_books = set(all_books)

    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(all_books)}")
    print(f"unique_urls={len(unique_books)}")