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

import re

from .parser import MainScraper


class ParserProxyNova(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)

    @classmethod
    async def format_url(cls, url, zone: str = 'us', *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""           
        return url.replace('country-nl', f'country-{zone}')

    @classmethod
    async def format_raw(cls, html: str) -> list:
        """Parse text/html pages, customized method for the parser of this website"""
        results = []
        soup = BeautifulSoup(html, 'html.parser')

        # Find the table element
        table = soup.find('table', {'class': 'table'})

        # Find all rows in the table body
        rows = table.find('tbody').find_all('tr')

        for row in rows:
            # Initialize a dictionary for each row
            proxy_info = {}

            # Find all cells in the row
            cells = row.find_all(['td', 'th'])

            # Extract data from each cell and store it in the dictionary
            proxy_info['Proxy IP'] = '' if cells[0].abbr is None else await cls.execute_js(cells[0].abbr.script.string.strip())
            proxy_info['Proxy Port'] = cells[1].text.strip()
            proxy_info['Last Check'] = cells[2].text.strip()
            proxy_info['Proxy Speed'] = cells[3].text.strip()
            proxy_info['Uptime'] = cells[4].text.strip()
            proxy_info['Proxy Country'] = cells[5].text.strip()
            proxy_info['Anonymity'] = cells[6].text.strip()

            results.append(proxy_info)
        return results

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        if zone.upper() == 'NL':
            if len(data['Proxy IP']) > 0:
                queue.put({
                    'country': 'Netherlands',
                    'zone': 'NL',
                    'method': 'http',
                    'anonymity': 'anonymous' if data['Anonymity'].lower() in ['elite', 'anonymous', 'elite proxy'] else 'transparent',
                    'protocol': 'http',
                    'port': str(data['Proxy Port']),
                    'ip': data['Proxy IP'],
                })
        return queue
    
    @classmethod
    async def restore_js_commands(cls, commands: tuple) -> tuple:
        """Rebuild broken javascript methods (ES6)"""
        process_queue = Queue()
        results = []
        for command in commands: process_queue.put(command)
        prev_command = ''
        while not process_queue.empty():
            command = process_queue.get()
            lefties = int(len([char for char in command if char == '(']))
            righties = int(len([char for char in command if char == ')']))
            if lefties == righties:
                results.append(command)
            elif lefties > righties:
                prev_command = f'{prev_command}.{command}'
                process_queue.put(prev_command)
            elif righties > lefties:
                if len(prev_command) > 0:
                    prev_command = f'{prev_command}.{command}'
                    process_queue.put(prev_command)
                else:
                    results.append(command[:len(command) - (righties - lefties)])
        return tuple(results)

    @classmethod
    async def execute_js(cls, js_code):
        """Try to figure out the IP address, This website hides it behind javascript, here we decode it."""
        ## Extract IP Hash
        ip_hash = js_code.replace('document.write("', '').split('".').pop(0)
        broken_commands = tuple([ f'{i})' for i in js_code.replace(ip_hash, '').replace('document.write("".', '')[:len(js_code.replace(ip_hash, '').replace('document.write(""', '')) - 1].split(').') if len(i) > 0])
        ip_encoding = await cls.restore_js_commands(broken_commands)
        for operation in ip_encoding:
            # Convert substring
            if re.search(r'split\(""\)', operation) is not None:
                ip_hash = tuple([char for char in ip_hash])
            elif re.search(r'reverse\(\)', operation) is not None:
                ip_hash = ip_hash[::-1]
            elif re.search(r'join\(""\)', operation) is not None:
                ip_hash = "".join(ip_hash)
            elif re.search(r'substring\(\d+(\+|\-|\*|\/)\d+, \d+(\+|\-|\*|\/)\d+\)', operation) is not None:
                _int, _end = operation.replace('substring(', '').replace(')', '').split(', ')
                if _int.startswith('".'): _int = _int.replace('".', '0')
                if _end.startswith('".'): _end = _end.replace('".', '0')
                _int = eval(_int)
                _end = eval(_end)
                ip_hash = ip_hash[_int:_end]
            else:
                raise NotImplemented(operation)
        return ip_hash
