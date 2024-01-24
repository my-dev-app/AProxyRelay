# -*- mode: python ; coding: utf-8 -*-
"""
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
------------------------------------
Targets proxynova.com:

    - https://www.proxynova.com/proxy-server-list/country-nl
"""
from bs4 import BeautifulSoup


class ParserProxyNova(object):
    def __init__(self, data: dict = None) -> None:
        self.data = data
        if self.data is None: raise AttributeError('DATA is Required')

    def _get_protocol(self, protocol: int):
        prot = 'unknown'
        if protocol == 1 or protocol == 2:
            prot = 'http'
        elif protocol == 2:
            prot = 'https'
        elif protocol == 4:
            prot = 'Socks4'
        elif protocol == 8:
            prot = 'Socks5'
        return prot.lower()

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

        # Find the table with the given ID
        table = soup.find('table', {'id': 'tbl_proxy_list'})

        listed = []

        if table:
            # Extract data from the table rows
            for row in table.select('tbody tr'):
                # Extracting data from each column in the row
                ip = row.select_one('td[title] abbr')
                ip = ip['title'] if ip and 'title' in ip.attrs else None

                port = row.select_one('td:nth-of-type(2)')
                port = port.text.strip() if port else None

                # Do something with the extracted data (e.g., print it)
                # print(f"IP: {ip}, Port: {port}, Last Check: {last_check}, Proxy Speed: {proxy_speed}, Uptime: {uptime_percent}, Country: {country_name}, Anonymity: {anonymity}")
                if ip is not None:
                    listed.append({
                        'ip': f"socks4://{ip}" if port is None else f"socks4://{ip}:{port}",
                        'ssl': False,
                        'protocol': "socks4",
                    })
                    listed.append({
                        'ip': f"socks5://{ip}" if port is None else f"socks5://{ip}:{port}",
                        'ssl': False,
                        'protocol': "socks5",
                    })
                    listed.append({
                        'ip': f"http://{ip}" if port is None else f"http://{ip}:{port}",
                        'ssl': False,
                        'protocol': "http",
                    })

        return {'data': listed}
