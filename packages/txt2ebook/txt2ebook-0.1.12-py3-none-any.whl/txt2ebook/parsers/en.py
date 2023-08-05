# pylint: disable=too-few-public-methods
"""
Copyright (C) 2021,2022 Kian-Meng Ang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from loguru import logger

from ..models import Book
from .base import BaseParser


STRUCTURE_NAMES = {
    "cover": "Cover",
}


class EnParser(BaseParser):
    """
    Module for parsing English content txt file.
    """

    re_volume: str = "^Volume.*$"
    re_chapter: str = "^Chapter.*$"

    def __init__(self, content: str, config: dict) -> None:
        self.raw_content = content
        self.book_title = config.title
        self.authors = config.author
        self.cover = config.cover
        self.delete_regex = config.delete_regex
        self.replace_regex = config.replace_regex
        self.delete_line_regex = config.delete_line_regex
        self.no_wrapping = config.no_wrapping
        self.width = config.width

    def parse(self) -> Book:
        """
        Parse the content into volumes (optional) and chapters.
        """
        massaged_content = self.massage()
        (parsed_content, volumes, chapters) = self.parse_content(
            massaged_content
        )

        return Book(
            title=self.detect_book_title(),
            language="en",
            authors=self.detect_authors(),
            cover=self.cover,
            raw_content=self.raw_content,
            massaged_content=massaged_content,
            parsed_content=parsed_content,
            volumes=volumes,
            chapters=chapters,
            structure_names=STRUCTURE_NAMES,
        )

    def massage(self) -> str:
        """
        Massage the content.
        """
        return self.raw_content

    def detect_book_title(self):
        """
        Detect the book title.
        """
        return self.book_title

    def detect_authors(self):
        """
        Detect the book authors.
        """
        return self.authors
