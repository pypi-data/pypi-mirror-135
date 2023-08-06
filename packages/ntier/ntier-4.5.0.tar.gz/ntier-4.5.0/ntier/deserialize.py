"""Data deserialization methods."""
import base64
import datetime
import decimal
from typing import Any, Callable, List, Mapping, NamedTuple, Optional, Union
from uuid import UUID

from .deserialize_html import (HtmlAttributes, HtmlStripper, HtmlTags,
                               default_html_stripper)

Map = Callable[[Any], Any]
Record = Mapping[str, Any]


class MapDef(NamedTuple):
    extract: Map
    map: Map
    key: str


class Attr(str):
    pass


Key = Union[str, Attr]

TRUTHY = {True, "t", "true", "y", "yes", "1", 1}
FALSEY = {False, "f", "false", "n", "no", "0", 0}
NOT_FOUND = object()


class Deserialize:
    """Contains deserialization methods. They take API data and turn it into domain data."""

    html_stripper: HtmlStripper = default_html_stripper

    @staticmethod
    def attr(key: str) -> Attr:
        return Attr(key)

    @staticmethod
    def map_def(extract: Map, map: Map, key: Key) -> MapDef:
        return MapDef(extract, map, key)

    @classmethod
    def register_html_stripper(cls, html_stripper: HtmlStripper) -> None:
        cls.html_stripper = html_stripper

    @classmethod
    def key(
        cls,
        key: Key,
        map: Map,
        output_key: Optional[str] = None,
        fallback: Any = NOT_FOUND,
    ) -> MapDef:
        """Create a MapDef that pulls from a top-level key on a Mapping."""

        def extract(data: Record) -> Any:
            return data.get(key, fallback)

        return cls.map_def(extract, map, output_key or key)

    @classmethod
    def path(
        cls,
        keys: List[Key],
        map: Map,
        output_key: Optional[str] = None,
        fallback: Any = NOT_FOUND,
    ) -> MapDef:
        """Create a MapDef that pulls from a path in nested Mappings.

        if output_key is not specified, the last value in keys is used.
        """

        def extract(data: Record) -> Any:
            parts = iter(keys)
            value = data
            while True:
                try:
                    key = next(parts)
                except StopIteration:
                    return value

                if isinstance(key, Attr):
                    if hasattr(value, key):
                        value = getattr(value, key)
                    else:
                        return fallback
                else:
                    if key in value:
                        value = value[key]
                    else:
                        return fallback

        return cls.map_def(extract, map, output_key or keys[-1])

    @classmethod
    def map(
        cls, map_defs: Union[List[MapDef], Mapping[str, Map]]
    ) -> Callable[[Any], Record]:
        """Retrurns a function that will map any input into a mapping."""

        def mapper(data: Any) -> Record:
            if data is None:
                return {}

            if isinstance(map_defs, list):
                output = {}
                for map_def in map_defs:
                    value = map_def.extract(data)
                    if value is NOT_FOUND:
                        continue
                    output[map_def.key] = map_def.map(value)
                return output

            return {k: v(data.get(k)) for (k, v) in map_defs.items()}

        return mapper

    @classmethod
    def list(cls, fn: Map) -> Callable[[List], List]:
        """Returns a function that will apply a map to all items in a list."""

        def mapper(data: List) -> List:
            try:
                return [fn(val) for val in data]
            except TypeError:
                return []

        return mapper

    @classmethod
    def identity(cls, val: Any) -> Any:
        """Return the value as-is."""
        return val

    @classmethod
    def int(cls, val: Any) -> Optional[int]:
        """Try to parse a value as an integer."""
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def float(cls, val: Any) -> Optional[float]:
        """Try to parse a value as a float."""
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def date(cls, val: Any) -> Optional[datetime.date]:
        """Try to parse a value as an ISO date."""
        try:
            return datetime.date.fromisoformat(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def bool(cls, val: Any) -> Optional[bool]:
        """Try to parse a value as a truthy value."""
        if isinstance(val, str):
            val = val.lower()
        if val in TRUTHY:
            return True
        if val in FALSEY:
            return False
        return None

    @classmethod
    def datetime(cls, val: Any) -> Optional[datetime.datetime]:
        """Try to parse a value as an ISO datetime."""
        try:
            return datetime.datetime.fromisoformat(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def uuid(cls, val: Any) -> Optional[UUID]:
        """Try to parse a value as an UUID."""
        if isinstance(val, UUID):
            return val
        try:
            return UUID(val)
        except (ValueError, TypeError):
            return None

    @classmethod
    def decimal(cls, val: Any) -> Optional[decimal.Decimal]:
        """Try to parse a decimal."""
        try:
            return decimal.Decimal(val)
        except (decimal.InvalidOperation, TypeError, ValueError):
            return None

    @classmethod
    def text(cls, val: Any) -> Optional[str]:
        """Return a value as a string. This method does no HTML escaping, so it should
        only be used when HTML escaping is not a concern.
        """
        if val is None:
            return None
        sval = str(val).strip()
        if not sval:
            return None
        return sval

    @classmethod
    def _html_safe_text(
        cls, tags: HtmlTags, attributes: HtmlAttributes, val: Optional[str]
    ) -> Optional[str]:
        if val is None:
            return None

        val = str(val)
        if val is None:
            return None

        val = val.strip()
        if not val:
            return None

        val = cls.html_stripper(tags, attributes, val)

        return val

    @classmethod
    def html_safe_text(
        cls, *, tags: HtmlTags = None, attributes: HtmlAttributes = None
    ) -> Callable[[Optional[str]], Optional[str]]:
        """Maps a value to a string."""

        def mapper(val: Optional[str]) -> Optional[str]:
            return cls._html_safe_text(tags or [], attributes or {}, val)

        return mapper

    @classmethod
    def base64(cls, val: Any) -> Optional[bytes]:
        """Try to parse base64 to bytes."""
        try:
            val = base64.b64decode(val, validate=True)
            if not val:
                return None
            return val
        except (TypeError, ValueError):
            return None
