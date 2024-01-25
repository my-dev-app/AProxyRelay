# -*- mode: python ; coding: utf-8 -*-
"""
░░      ░░       ░░       ░░░      ░░  ░░░░  ░  ░░░░  ░       ░░        ░  ░░░░░░░░      ░░  ░░░░  ░
▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒▒  ▒▒  ▒▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒
▓  ▓▓▓▓  ▓       ▓▓       ▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓▓▓    ▓▓▓       ▓▓      ▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓
█        █  ███████  ███  ██  ████  ██  ██  █████  ████  ███  ██  ███████  ███████        ████  ████
█  ████  █  ███████  ████  ██      ██  ████  ████  ████  ████  █        █        █  ████  ████  ████
By undeƒined
------------

Main parser example, other parsers can inherit from this class
"""
from queue import Queue

from .core import ScraperCore


class MainScraper(ScraperCore):
    def __init__(self) -> None:
        ScraperCore.__init__(self)

    @classmethod
    async def format_raw(cls, html: str):
        """Parse text/html pages, customized method for the parser of this website"""
        raise NotImplemented('Format raw parser has not been implemented yet')

    @classmethod
    async def format_data(cls, data: dict, queue: Queue):
        """Data formatter, formats data and returns is back in the process Queue"""
        raise NotImplemented('Form data parser has not been implemented yet')
        # return queue.put({
        #     'country': 'US',
        #     'zone': 'US',
        #     'method': 'http',
        #     'anonymity': 'anonymous',
        #     'protocol': 'http',
        #     'port': '8080',
        #     'ip': '127.0.0.1',
        # })
