"""Contains the Paging data structure."""
import math
from typing import Optional

from ntier.constants import PAGE_DEFAULT, PER_PAGE_DEFAULT, PER_PAGE_MAX


class Paging:
    """Contains paging information."""

    def __init__(self, page: int, per_page: int, total_records: int = 0):
        if page < 0:
            raise ValueError("page must be 0 or greater")
        if per_page < 1:
            raise ValueError("per_page must be 1 or greater")
        if per_page > PER_PAGE_MAX:
            raise ValueError(f"per_page must be no greater than {PER_PAGE_MAX}")
        if total_records < 0:
            raise ValueError("total_records must be 0 or greater")

        self.page = page
        self.per_page = per_page
        self.total_records = total_records

    @classmethod
    def default(cls) -> "Paging":
        """Builds a default object."""
        return cls(PAGE_DEFAULT, PER_PAGE_DEFAULT)

    @classmethod
    def parse(cls, raw_page: Optional[str], raw_per_page: Optional[str]) -> "Paging":
        """Tries to parse paging from string values.

        Paging parameters often come in on the request as strings and need to be parsed as
        integers.
        """
        page: Optional[int] = None
        per_page: Optional[int] = None

        if raw_page:
            try:
                page = int(raw_page)
            except ValueError:
                page = PAGE_DEFAULT
        else:
            page = PAGE_DEFAULT
        if raw_per_page:
            try:
                per_page = int(raw_per_page)
            except ValueError:
                per_page = PER_PAGE_DEFAULT
        else:
            per_page = PER_PAGE_DEFAULT

        return cls(page, per_page)

    @property
    def limit(self) -> int:
        """Returns the limit based on the paging."""
        return self.per_page

    @property
    def offset(self) -> int:
        """Returns the offset based on the paging."""
        return (self.page - 1) * self.per_page

    @property
    def total_pages(self) -> int:
        """Return the total number of pages."""
        if self.total_records == 0:
            return 0
        return math.ceil(self.total_records / self.per_page)

    def set_total_records(self, value: int) -> "Paging":
        """Sets the total records."""
        if value < 0:
            raise ValueError("total_records must be 0 or greater")
        self.total_records = value
        return self
