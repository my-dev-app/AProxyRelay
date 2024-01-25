# -*- mode: python ; coding: utf-8 -*-
"""
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
------------------------------------
Targets spys.one:

    - https://spys.one/free-proxy-list/NL/
"""
from bs4 import BeautifulSoup

import re


class ParserSpys(object):
    def __init__(self, data: dict = None) -> None:
        self.data = data
        if self.data is None: raise AttributeError('DATA is Required')

    def _validate_ip_address(self, ip):
        # Regular expression for a valid IPv4 or IPv6 address
        ip_regex = r'^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$|^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'

        if re.match(ip_regex, ip):
            # Valid IP address
            return True
        else:
            # Invalid IP address
            return False

    async def _parse(self):
        try:
            return [
                item
                for item in 
                self.data['data']
            ]
        except Exception as e:
            print(f'Error found in ParserProxyNova: {e.args}')
            return []

    @classmethod
    async def _scrape(cls, response):
        html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')

        listed = []

        # Find the table with the given structure
        table = soup.find('table', {'width': '100%', 'border': '0', 'cellspacing': '0', 'cellpadding': '1'})

        if table:
            # Extract data from the table rows
            rows = table.select('tr[class^="spy"]')
            headers_row = rows[1]

            # Extract headers from the headers row
            headers = [header.text.strip() for header in headers_row.select('td')]

            # Extract data from the remaining rows
            for row in rows[2:]:
                row_data = [data.text.strip() for data in row.select('td')]

                # Combine headers with row data and create a dictionary
                data_dict = dict(zip(headers, row_data))
                if cls._validate_ip_address(cls, data_dict['Proxy address:port']):
                    listed.append(data_dict)

        return {'data': [
            {
                'ip': f"{'http' if 'http' in item['Proxy type'].lower() else item['Proxy type'].lower()}://{item['Proxy address:port']}",
                'ssl': False,
                'protocol': 'http' if 'http' in item['Proxy type'].lower() else item['Proxy type'].lower(),
            }
            for item in listed
        ]}
