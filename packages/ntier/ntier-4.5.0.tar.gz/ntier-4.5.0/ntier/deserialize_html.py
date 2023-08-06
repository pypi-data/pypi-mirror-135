"""This module provides base implementations for HTML stripping.

The default implementation will use bleach if it is installed, otherwise an overly aggressive,
very simple html stripper is employed.
"""
import re
from typing import Callable, List, Mapping

import bleach

HtmlTags = List[str]
HtmlAttributes = Mapping[str, List[str]]

HtmlStripper = Callable[[HtmlTags, HtmlAttributes, str], str]


_html_re = re.compile(r"""<[^>]*?>""")


def naive_html_stripper(_: HtmlTags, __: HtmlAttributes, val: str) -> str:
    return _html_re.sub("", val)


def bleach_html_stripper(tags: HtmlTags, attributes: HtmlAttributes, val: str) -> str:
    """Exclude tags and attributes using BeautifulSoup4."""
    return bleach.clean(val, tags, attributes, strip=True, strip_comments=True)


def default_html_stripper(tags: HtmlTags, attributes: HtmlAttributes, val: str) -> str:
    return bleach_html_stripper(tags, attributes, val)
