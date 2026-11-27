"""Parser for the FP4All inverter errorlog.htm page."""

from __future__ import annotations

from html.parser import HTMLParser


_FIELDS = (
    "date_time",
    "recovery",
    "mode",
    "m_number",
    "code",
    "message",
    "description",
    "value",
)


class _ErrorLogHTMLParser(HTMLParser):
    """Extract the eight-column error rows from errorlog.htm."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag == "tr":
            self._row = []
        elif tag == "td" and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_entityref(self, name: str) -> None:
        if self._cell is not None:
            self._cell.append(f"&{name};")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "td" and self._cell is not None and self._row is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if len(self._row) == 8:
                self.rows.append(self._row)
            self._row = None
            self._cell = None


def parse_errorlog(html: str) -> list[dict[str, str]]:
    """Return error rows in the same newest-first order as the logger page."""
    parser = _ErrorLogHTMLParser()
    parser.feed(html)

    errors: list[dict[str, str]] = []
    for row in parser.rows:
        # Skip the HTML table header.
        if row[0].strip().lower() == "date/time":
            continue

        errors.append(dict(zip(_FIELDS, row)))

    return errors

