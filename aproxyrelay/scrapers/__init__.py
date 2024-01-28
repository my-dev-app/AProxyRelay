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
from .parser_gg_my_dev_app import ParserGGMyDevApp
from .parser_lumiproxy import ParserLumiProxy
from .parser_proxyscrape import ParserProxyScrape
from .parser_socks_proxy import ParserSocksProxy
from .parser_spys_de import ParserSpysDE
from .parser_spys_nl import ParserSpysNL
from .parser_spys_us import ParserSpysUS
from .parser_ssl_proxies import ParserSSLProxies


proxy_list = [
    {
        'url': 'https://free-proxy-list.net/',
        'parser': ParserFreeProxyList,
    },
    {
        'url': 'https://api.lumiproxy.com/web_v1/free-proxy/list?page_size=10000&page=1&country_code=nl',
        'parser': ParserLumiProxy,
    },
    {
        'url': 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=all&country=NL&anonymity=all&timeout=15000&proxy_format=ipport&format=json',  # noqa: B950
        'parser': ParserProxyScrape,
    },
    {
        'url': 'https://socks-proxy.net/',
        'parser': ParserSocksProxy,
    },
    {
        'url': 'https://spys.one/free-proxy-list/DE/',
        'parser': ParserSpysDE,
    },
    {
        'url': 'https://spys.one/free-proxy-list/NL/',
        'parser': ParserSpysNL,
    },
    {
        'url': 'https://spys.one/free-proxy-list/US/',
        'parser': ParserSpysUS,
    },
    {
        'url': 'https://www.sslproxies.org/',
        'parser': ParserSSLProxies,
    },
    {
        'url': 'https://gg.my-dev.app/api/v1/proxies/available?zone=nl&anonimity=all&protocol=all&page=1&size=1000',
        'parser': ParserGGMyDevApp,
    },
]
