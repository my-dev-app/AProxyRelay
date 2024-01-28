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


class ParserSpysNL(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)

    @classmethod
    async def format_url(cls, url, zone: str = 'us', *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        return url

    @classmethod
    async def format_raw(cls, html: str) -> list:
        """Parse text/html pages, customized method for the parser of this website"""
        results = []
        # Parse the HTML content of the page
        soup = BeautifulSoup(html, 'html.parser')

        # Find all rows containing proxy information
        rows = soup.find_all('tr', class_=['spy1xx', 'spy1x'])

        # Iterate through data rows
        for row in rows:
            # Extract all cells in the row
            cells = row.find_all('td', recursive=False)

            # Check if the row contains proxy data
            if len(cells) == 9:
                # Create a dictionary with relevant data
                data_dict = {
                    'Proxy': None if not cells[0].find('font', class_='spy14') else cells[0].find('font', class_='spy14').text.strip(),  # noqa: B950
                    'Type': None if not cells[1].find('font', class_='spy1') else cells[1].find('font', class_='spy1').text.strip(),  # noqa: B950
                    'Anonymity': None if not cells[2].find('font', class_='spy5') else cells[2].find('font', class_='spy5').text.strip(),  # noqa: B950
                    'Country': None if not cells[3].find('font', class_='spy14') else cells[3].find('font', class_='spy14').text.strip(),  # noqa: B950
                    'Hostname/ORG': None if not cells[4].find('font', class_='spy1') else cells[4].find('font', class_='spy1').text.strip(),  # noqa: B950
                    'Latency': None if not cells[5].find('font', class_='spy1') else cells[5].find('font', class_='spy1').text.strip(),  # noqa: B950
                    'Speed': None if not cells[6].find('font', class_='spy1') else cells[6].find('font', class_='spy1').text.strip(),  # noqa: B950
                    'Uptime': None if not cells[7].find('font', class_='spy1') else cells[7].find('font', class_='spy1').text.strip(),  # noqa: B950
                    'Check Date': None if not cells[8].find('font', class_='spy1') else cells[8].find('font', class_='spy1').text.strip(),  # noqa: B950
                }
                if data_dict['Proxy'] is not None:
                    results.append(data_dict)

        return results

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        if zone.upper() == 'NL':
            queue.put({
                'country': 'Netherlands',
                'zone': 'NL',
                'method': 'http' if data['Type'] is None else data['Type'].lower(),
                'anonymity': 'anonymous' if data['Anonymity'] is not None else 'transparent',
                'protocol': 'http' if data['Type'] is None else data['Type'].lower(),
                'port': '' if len(data['Proxy'].split(':')) <= 1 else data['Proxy'].split(':')[1],
                'ip': data['Proxy'].split(':')[0],
            })
        return queue
