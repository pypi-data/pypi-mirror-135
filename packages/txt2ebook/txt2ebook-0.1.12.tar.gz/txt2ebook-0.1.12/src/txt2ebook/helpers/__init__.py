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

import sys
from importlib import import_module
from typing import Any

from loguru import logger


def to_classname(words: str, suffix: str) -> str:
    """
    Generate class name from words.
    """
    return words.replace("-", " ").title().replace(" ", "") + suffix


def load_class(package_name: str, class_name: str) -> Any:
    """
    Load class dynamically.
    """
    try:
        package = import_module(package_name)
        klass = getattr(package, class_name)
        logger.debug("Load module: {}.{}", package_name, class_name)
        return klass
    except AttributeError:
        logger.error("Fail to load module: {}.{}", package_name, class_name)
        sys.exit()
