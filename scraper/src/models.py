from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime


class Book(BaseModel):
    title: str = Field(min_length=1)

    product_url: HttpUrl

    price_text: str = Field(min_length=1)

    availability_text: str = Field(min_length=1)

    rating_text: str = Field(min_length=1)

    description: Optional[str] = None

    source_page: HttpUrl

    fetched_at: datetime

    category: Optional[str] = None

    # Normalized fields
    price_gbp: float
    stock_count: int
    in_stock: bool
    rating: int