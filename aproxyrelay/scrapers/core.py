# -*- mode: python ; coding: utf-8 -*-
"""
░░      ░░       ░░       ░░░      ░░  ░░░░  ░  ░░░░  ░       ░░        ░  ░░░░░░░░      ░░  ░░░░  ░
▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒▒  ▒▒  ▒▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒
▓  ▓▓▓▓  ▓       ▓▓       ▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓▓▓    ▓▓▓       ▓▓      ▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓
█        █  ███████  ███  ██  ████  ██  ██  █████  ████  ███  ██  ███████  ███████        ████  ████
█  ████  █  ███████  ████  ██      ██  ████  ████  ████  ████  █        █        █  ████  ████  ████
By undeƒined
------------

Core of the proxy relay, contains async within the library
"""
from queue import Queue

import logging


# Configure the logger
logging.basicConfig(level=logging.INFO)


class ScraperCore(object):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    @classmethod
    async def scrape(cls, zone, response):
        if response.content_type == 'application/json':
            data = await response.json()
        elif response.content_type == 'text/html':
            data = await response.text()
            data = await cls.format_raw(data)
        elif response.content_type == 'text/plain':
            data = await response.content.read()
            data = await cls.format_raw(data.decode())
        else:
            raise ReferenceError(f'None exiting content type for parser: {response.content_type}')
        queue = await cls._flatten_response(data)
        return await cls._format_queue(zone, queue)

    @classmethod
    async def _flatten_response(cls, data) -> Queue:
        """Flat response data into a Queue ready to be parsed into a pre-set json scheme"""
        results = Queue()
        if type(data) is list:
            for item in data:
                results.put(item)
        else:
            results.put(data)
        return results

    @classmethod
    async def _format_queue(cls, zone: str, queue: Queue) -> Queue:
        """
        Formats queue into a pre-set json scheme

        {
            'zone': str,
            'method': str['http', 'https', 'socks4', 'socks5', 'unknown',],
            'anonymity': str['anonymous', 'transparent',],
            'protocol': str['http', 'https', 'socks4', 'socks5'],
            'port': str,
            'ip': str,
        }
        """
        results = Queue()
        while not queue.empty():
            data = queue.get()
            results = await cls.format_data(zone, data, results)
        return results
