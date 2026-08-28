import re


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def normalize_price(price_text: str) -> float:
    return float(price_text.replace("£", ""))


def normalize_stock(availability_text: str):
    match = re.search(r"(\d+)", availability_text)

    stock_count = int(match.group(1)) if match else 0

    in_stock = "In stock" in availability_text

    return stock_count, in_stock


def normalize_rating(rating_text: str) -> int:
    return RATING_MAP[rating_text]