# pylint: disable=too-few-public-methods
"""
Module for parsing Traditional Chinese language txt file.
"""
from .zhcn import ZhCnParser


class ZhTwParser(ZhCnParser):
    """
    Module for parsing txt format in zh-tw.
    """
