# -*- mode: python ; coding: utf-8 -*-
"""
░░      ░░       ░░       ░░░      ░░  ░░░░  ░  ░░░░  ░       ░░        ░  ░░░░░░░░      ░░  ░░░░  ░
▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒▒  ▒▒  ▒▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒
▓  ▓▓▓▓  ▓       ▓▓       ▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓▓▓    ▓▓▓       ▓▓      ▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓
█        █  ███████  ███  ██  ████  ██  ██  █████  ████  ███  ██  ███████  ███████        ████  ████
█  ████  █  ███████  ████  ██      ██  ████  ████  ████  ████  █        █        █  ████  ████  ████
By undeƒined
------------

Proxy list and their mapped scrapers
"""
from .parser_freeproxylist import ParserFreeProxyList
from .parser_lumiproxy import ParserLumiProxy


proxy_list = [
    {
        'url': 'https://free-proxy-list.net/',
        'parser': ParserFreeProxyList,
    },
    {
        'url': 'https://api.lumiproxy.com/web_v1/free-proxy/list?page_size=10000&page=1&country_code=nl',
        'parser': ParserLumiProxy,
    },
    # {
    #     'url': 'https://www.proxynova.com/proxy-server-list/country-nl',
    #     'parser': ParserProxyNova,
    # },
    # {
    #     'url': 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&country=NL&anonymity=all&timeout=15000&proxy_format=ipport&format=json',
    #     'parser': ParserProxyScrape,
    # },
    # {
    #     'url': 'https://socks-proxy.net/',
    #     'parser': ParserSocksProxy,
    # },
    # {
    #     'url': 'https://spys.one/free-proxy-list/NL/',
    #     'parser': ParserSpys,
    # },
    # {
    #     'url': 'https://www.sslproxies.org/',
    #     'parser': ParserSSLProxies,
    # },
    # {
    #     'url': 'https://gg.my-dev.app/api/v1/steam/filter/genres/',
    #     'parser': ParserFreeProxyList,
    # },
]