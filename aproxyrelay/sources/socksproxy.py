# -*- mode: python ; coding: utf-8 -*-
"""
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
------------------------------------
Targets socks-proxy.net:

    - https://socks-proxy.net/
"""
import lxml.html as lh


class ParserSocksProxy(object):
    def __init__(self, data: dict = None) -> None:
        self.data = data
        if self.data is None: raise AttributeError('DATA is Required')

    async def _parse(self):
        try:
            return [
                item
                for item in 
                self.data['data']
            ]
        except Exception as e:
            print(f'Error found in ParserSocksProxy: {e.args}')
            return []

    @classmethod
    async def _scrape(cls, response):
        html = await response.text()
        doc = lh.fromstring(html)
        tr_elements = doc.xpath('//*[@id="list"]//tr')
        listed = [{
            'ip': f'socks5://{tr_elements[i][0].text_content()}:{tr_elements[i][1].text_content()}',
            'ssl': tr_elements[i][6].text_content().lower() == 'yes',
            'protocol': "http",
        } for i in range(1, len(tr_elements)) if cls.__criteria(cls, tr_elements[i])] + [{
            'ip': f'socks4://{tr_elements[i][0].text_content()}:{tr_elements[i][1].text_content()}',
            'ssl': tr_elements[i][6].text_content().lower() == 'yes',
            'protocol': "http",
        } for i in range(1, len(tr_elements)) if cls.__criteria(cls, tr_elements[i])]
        return {'data': listed}

    def __criteria(self, row_elements):
        """Check origin country"""
        country = row_elements[2].text_content()
        if country.lower() == 'nl':
            return True
        return False
