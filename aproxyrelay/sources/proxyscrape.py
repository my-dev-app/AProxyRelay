# -*- mode: python ; coding: utf-8 -*-
"""
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
------------------------------------
Targets proxyscrape.com:

    - https://proxyscrape.com/free-proxy-list
    - https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&country=NL&anonymity=all&timeout=15000&proxy_format=ipport&format=json
"""
class ParserProxyScrape(object):
    def __init__(self, data: dict = None) -> None:
        self.data = data
        if self.data is None: raise AttributeError('DATA is Required')

    async def _parse(self):
        try:
            return [
                {
                    'ip': f"{item['protocol'].lower()}://{item['proxy']}",
                    'ssl': item['ssl'],
                    'protocol': item['protocol'],
                }
                for item in 
                self.data['proxies']
            ]
        except Exception as e:
            print(f'Error found in ParserProxyScrape: {e.args}')
            return []
