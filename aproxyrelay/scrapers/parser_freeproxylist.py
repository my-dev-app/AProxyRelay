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
import lxml.html as lh
from queue import Queue

from .parser import MainScraper


class ParserFreeProxyList(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)

    @classmethod
    async def format_raw(cls, html: str):
        """Parse text/html pages, customized method for the parser of this website"""
        return html

    @classmethod
    async def format_data(cls, data: dict, queue: Queue):
        """Data formatter, formats data and returns is back in the process Queue"""
        return {
            'country': 'US',
            'zone': 'US',
            'method': 'http',
            'anonymity': 'anonymous',
            'protocol': 'http',
            'port': '8080',
            'ip': '127.0.0.1',
        }



# class ParserFreeProxyList(object):
#     def __init__(self, data: dict = None) -> None:
#         self.data = data
#         if self.data is None: raise AttributeError('DATA is Required')

#     async def _parse(self):
#         try:
#             return [
#                 item
#                 for item in 
#                 self.data['data']
#             ]
#         except Exception as e:
#             print(f'Error found in ParserFreeProxyList: {e.args}')
#             return []

#     @classmethod
#     async def _scrape(cls, response):
#         html = await response.text()
#         doc = lh.fromstring(html)
#         tr_elements = doc.xpath('//*[@id="list"]//tr')
#         listed = [{
#             'ip': f'http://{tr_elements[i][0].text_content()}:{tr_elements[i][1].text_content()}',
#             'ssl': tr_elements[i][6].text_content().lower() == 'yes',
#             'protocol': "http",
#         } for i in range(1, len(tr_elements)) if cls.__criteria(cls, tr_elements[i])]
#         return {'data': listed}

#     def __criteria(self, row_elements):
#         """Check origin country"""
#         country = row_elements[2].text_content()
#         if country.lower() == 'nl':
#             return True
#         return False
