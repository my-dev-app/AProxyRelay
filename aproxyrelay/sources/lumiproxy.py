# -*- mode: python ; coding: utf-8 -*-
"""
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
------------------------------------
Targets lumiproxy.com:

    - https://www.lumiproxy.com/free-proxy/
    - https://api.lumiproxy.com/web_v1/free-proxy/list?page_size=10000&page=1&country_code=nl
"""
class ParserLumiProxy(object):
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
                {
                    'ip': f"{self._get_protocol(item['protocol'])}://{item['ip']}:{item['port']}",
                    'ssl': bool(item['google_passed']),
                    'protocol': self._get_protocol(item['protocol']),
                }
                for item in 
                self.data['data']['list']
            ]
        except Exception as e:
            print(f'Error found in ParserLumiProxy: {e.args}')
            return []
