# -*- mode: python ; coding: utf-8 -*-
"""
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
------------------------------------
Contains various sources for proxies
"""
from .proxynova import ParserProxyNova
from .lumiproxy import ParserLumiProxy
from .proxyscrape import ParserProxyScrape


_proxy_list = [
    {
        'url': 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&country=NL&anonymity=all&timeout=15000&proxy_format=ipport&format=json',
        'parser': ParserProxyScrape,
    },
    {
        'url': 'https://api.lumiproxy.com/web_v1/free-proxy/list?page_size=10000&page=1&country_code=nl',
        'parser': ParserLumiProxy,
    },
    {
        'url': 'https://www.proxynova.com/proxy-server-list/country-nl',
        'parser': ParserProxyNova,
    },
]

__all__ = [
    ParserProxyNova,
    ParserLumiProxy,
    ParserProxyScrape,
]
