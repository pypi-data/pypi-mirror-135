"""
Module for parsing Simplified Chinese language txt file.
"""
import cjkwrap
import regex as re
from loguru import logger

from ..models import Book
from .base import BaseParser


IDEOGRAPHIC_SPACE = "\u3000"
SPACE = "\u0020"
NUMS_WORDS = "零一二三四五六七八九十百千两"
FULLWIDTH_NUMS = "０１２３４５６７８９"

RE_TITLE = r"书名：(.*)|【(.*)】|《(.*)》"
RE_AUTHOR = r"作者：(.*)"
RE_NUMS = f"[.0-9{FULLWIDTH_NUMS}{NUMS_WORDS}]"

STRUCTURE_NAMES = {
    "cover": "封面",
}


class ZhCnParser(BaseParser):
    """
    Module for parsing txt format in zh-cn.
    """

    re_volume: str = f"^第{RE_NUMS}*[集卷册][^。~\n]*$"
    re_chapter: str = "|".join(
        [
            f"^第{RE_NUMS}*[章篇回折].*$",
            "^[楔引]子[^，].*$",
            "^序[章幕曲]?$",
            "^前言.*$",
            "^[内容]*简介.*$",
            "^[号番]外篇.*$",
            "^尾声$",
        ]
    )

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
            language="zh-cn",
            authors=self.detect_authors(),
            cover=self.cover,
            raw_content=self.raw_content,
            massaged_content=massaged_content,
            parsed_content=parsed_content,
            volumes=volumes,
            chapters=chapters,
            structure_names=STRUCTURE_NAMES,
        )

    def detect_book_title(self) -> str:
        """
        Extract book title from the content of the txt file.
        """
        if self.book_title:
            return self.book_title

        match = re.search(RE_TITLE, self.raw_content)
        if match:
            book_title = next(
                (title.strip() for title in match.groups() if title)
            )
            logger.info("Found book title: {}", book_title)
            return book_title

        logger.info("No book title found from file!")
        return ""

    def detect_authors(self) -> list:
        """
        Extract author from the content of the txt file.
        """
        if self.authors:
            return self.authors

        match = re.search(RE_AUTHOR, self.raw_content)
        if match:
            author = match.group(1).strip()
            logger.info("Found author: {}", author)
            return [author]

        logger.info("No author found from file!")
        return []

    def massage(self) -> str:
        """
        Massage the txt content.
        """
        content = self.raw_content

        content = BaseParser.to_unix_newline(content)

        if self.delete_regex:
            content = self.do_delete_regex(content)

        if self.replace_regex:
            content = self.do_replace_regex(content)

        if self.delete_line_regex:
            content = self.do_delete_line_regex(content)

        if self.no_wrapping:
            content = self.do_no_wrapping(content)

        if self.width:
            content = self.do_wrapping(content)

        return content

    def do_no_wrapping(self, content: str) -> str:
        """
        Remove wrapping. Paragraph should be in one line.
        """
        # Convert to single spacing before we removed wrapping.
        lines = content.split("\n")
        content = "\n\n".join([line.strip() for line in lines if line])

        unwrapped_content = ""
        for line in content.split("\n\n"):
            # if a line contains more opening quote(「) than closing quote(」),
            # we're still within the same paragraph.
            # e.g.:
            # 「...」「...
            # 「...
            if line.count("「") > line.count("」"):
                unwrapped_content = unwrapped_content + line.strip()
            elif (
                re.search(r"[…。？！]{1}」?$", line)
                or re.search(r"」$", line)
                or re.match(r"^[ \t]*……[ \t]*$", line)
                or re.match(r"^「」$", line)
                or re.match(r".*[》：＊\*]$", line)
                or re.match(r".*[a-zA-Z0-9]$", line)
            ):
                unwrapped_content = unwrapped_content + line.strip() + "\n\n"
            elif re.match(self.re_chapter, line):
                # replace full-width space with half-wdith space.
                # looks nicer on the output.
                header = line.replace(IDEOGRAPHIC_SPACE * 2, SPACE).replace(
                    IDEOGRAPHIC_SPACE, SPACE
                )
                unwrapped_content = (
                    unwrapped_content + "\n\n" + header.strip() + "\n\n"
                )
            else:
                unwrapped_content = unwrapped_content + line.strip()

        return unwrapped_content

    def do_wrapping(self, content: str) -> str:
        """
        Wrapping and filling CJK text.
        """
        logger.info("Wrapping paragraph to width: {}", self.width)

        paragraphs = []
        # We don't remove empty line and keep all formatting as it.
        for paragraph in content.split("\n"):
            paragraph = paragraph.strip()

            lines = cjkwrap.wrap(paragraph, width=self.width)
            paragraph = "\n".join(lines)
            paragraphs.append(paragraph)

        wrapped_content = "\n".join(paragraphs)
        return wrapped_content
