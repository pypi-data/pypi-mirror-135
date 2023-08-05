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
from dataclasses import dataclass, field
from typing import List


@dataclass(repr=False)
class Chapter:
    """
    A chapter class model.
    """

    title: str = field(default="")
    raw_content: str = field(default="", repr=False)
    paragraphs: List[str] = field(default_factory=List, repr=False)

    def __repr__(self):
        return "{}(title='{}', raw_content='{}')".format(
            self.__class__.__name__,
            self.title,
            self.raw_content[0:5].strip(),
        )
