
import json
from pathlib import Path
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from datetime import datetime, UTC


from models import Book
from normalize import (
    normalize_price,
    normalize_stock,
    normalize_rating,
)

BOOKS_URL = "https://books.toscrape.com/catalogue/page-1.html"


OUTPUT_DIR = Path("output")
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
    for attempt in range(2):

        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=5,
            )

            response.encoding = "utf-8"

            if response.status_code == 200:
                break

            if response.status_code in (500, 502, 503, 504) and attempt == 0:
                print("Retrying...")
                time.sleep(1)
                continue

            raise Exception(
                f"Request failed with status code {response.status_code}"
            )

        except requests.Timeout:

            if attempt == 0:
                print("Timeout. Retrying...")
                time.sleep(1)
                continue

            raise

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
        book_links.append({
         "product_url": absolute_url,
         "source_page": current_url,
})

    next_page = None

    next_link = soup.select_one("li.next a")

    if next_link:
        next_page = urljoin(current_url, next_link["href"])

    return book_links, next_page


def parse_book(html, product_url, source_page):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1").text.strip()

    price = soup.find("p", class_="price_color").text.strip()

    availability = (
        soup.find("p", class_="instock availability")
            .text
            .strip()
    )
    rating_element = soup.find("p", class_="star-rating")
    rating = rating_element["class"][1]

    breadcrumb = soup.find("ul", class_="breadcrumb")

    category = breadcrumb.find_all("li")[-2].text.strip()
    description_header = soup.find("div", id="product_description")

    description = ""

    fetched_at = datetime.now(UTC).isoformat()

    if description_header:
        description = description_header.find_next_sibling("p").text.strip()

    return {
    "title": title,
    "product_url": product_url,
    "price_text": price,
    "availability_text": availability,
    "rating_text": rating,
    "category": category,
    "description": description,
    "fetched_at": fetched_at,
    "source_page": source_page,
}

if __name__ == "__main__":

    run_start = time.time()

    started_at = datetime.now(UTC).isoformat()
    current_url = BOOKS_URL

    book_urls = []

    catalogue_pages = 0

    while current_url and catalogue_pages < 3:

        html = fetch_page(current_url)

        books, current_url = parse_catalogue(html, current_url)

        book_urls.extend(books)

        catalogue_pages += 1

        if current_url:
            time.sleep(0.5)


   


    books = []
    errors=[]
    failed_pages = 0

    for book_info in book_urls:

            raw_book = None
            try:
                html = fetch_page(book_info["product_url"])

                raw_book = parse_book(
                    html,
                    book_info["product_url"],
                    book_info["source_page"],
                )

                stock_count, in_stock = normalize_stock(
                    raw_book["availability_text"]
                )

            
                validated_book = Book(
                    **raw_book,
                    price_gbp=normalize_price(raw_book["price_text"]),
                    stock_count=stock_count,
                    in_stock=in_stock,
                    rating=normalize_rating(raw_book["rating_text"]),
                )

                books.append(
                validated_book.model_dump(
                    mode="json"
                    )
                )

            except Exception as e:
                failed_pages +=1
                errors.append(
                {
                    "product_url": book_info["product_url"],
                    "error": str(e),
                    "raw_record": raw_book,
                }
            )


    time.sleep(0.5)

    #print(len(books))
    print(f"Valid books: {len(books)}")
    print(f"Errors: {len(errors)}")
    if books:
            print(books[0])
    
    
    print(f"\ndetail_pages={len(books)}")
    OUTPUT_DIR.mkdir(exist_ok=True)

    

    with open(
    OUTPUT_DIR / "books.json",
    "w",
    encoding="utf-8",
    ) as file:
        json.dump(
            books,
            file,
            indent=2,
            ensure_ascii=False,
        )



    with open(
        OUTPUT_DIR / "errors.json",
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            errors,
            file,
            indent=2,
        )


    run_duration = round(time.time() - run_start, 2)

    report = {
        "started_at": started_at,
        "duration_seconds": run_duration,
        "catalogue_pages": catalogue_pages,
        "detail_pages": len(book_urls),
        "valid_records": len(books),
        "invalid_records": len(errors),
        "failed_pages": failed_pages,
    }

    with open(
        OUTPUT_DIR / "run-report.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
        )

















