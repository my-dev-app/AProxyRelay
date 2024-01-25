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
from .freeproxylist import ParserFreeProxyList
from .lumiproxy import ParserLumiProxy
from .proxynova import ParserProxyNova
from .proxyscrape import ParserProxyScrape
from .socksproxy import ParserSocksProxy
from .spys import ParserSpys
from .sslproxies import ParserSSLProxies


_proxy_list = [
    {
        'url': 'https://free-proxy-list.net/',
        'parser': ParserFreeProxyList,
    },
    {
        'url': 'https://api.lumiproxy.com/web_v1/free-proxy/list?page_size=10000&page=1&country_code=nl',
        'parser': ParserLumiProxy,
    },
    {
        'url': 'https://www.proxynova.com/proxy-server-list/country-nl',
        'parser': ParserProxyNova,
    },
    {
        'url': 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&country=NL&anonymity=all&timeout=15000&proxy_format=ipport&format=json',
        'parser': ParserProxyScrape,
    },
    {
        'url': 'https://socks-proxy.net/',
        'parser': ParserSocksProxy,
    },
    {
        'url': 'https://spys.one/free-proxy-list/NL/',
        'parser': ParserSpys,
    },
    {
        'url': 'https://www.sslproxies.org/',
        'parser': ParserSSLProxies,
    },
]

__all__ = [
    ParserFreeProxyList,
    ParserLumiProxy,
    ParserProxyNova,
    ParserProxyScrape,
    ParserSocksProxy,
    ParserSpys,
    ParserSSLProxies,
]
