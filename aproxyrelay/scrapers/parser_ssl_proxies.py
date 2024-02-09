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
from bs4 import BeautifulSoup
from queue import Queue

from .parser import MainScraper


class ParserSSLProxies(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)

    @classmethod
    async def format_url(cls, url, *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        cls.zone = kwargs.get("zone", "us")
        return url

    @classmethod
    async def format_raw(cls, html: str) -> list:
        """Parse text/html pages, customized method for the parser of this website"""
        results = []
        soup = BeautifulSoup(html, "html.parser")

        # Find the table with the given structure
        table = soup.find("table", {"class": "table table-striped table-bordered"})

        if table:
            # Extract headers from the table
            headers = [header.text.strip() for header in table.find_all("th")]

            # Extract data from the rows
            rows = table.find_all("tr")[1:]  # Skip the first row (header row)
            for row in rows:
                row_data = [data.text.strip() for data in row.find_all("td")]

                # Combine headers with row data and create a dictionary
                data_dict = dict(zip(headers, row_data, strict=True))
                results.append(data_dict)
        return results

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        if data['Code'] == zone.upper():
            queue.put({
                'zone': data['Code'],
                'method': 'https',
                'anonymity': 'anonymous' if data['Anonymity'].lower() in ['elite', 'anonymous', 'elite proxy'] else 'transparent',
                'protocol': 'https',
                'port': str(data['Port']),
                'ip': data['IP Address'],
            })
        return queue
