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
from .parser_multiproxy import ParserMultiProxy
from .parser_monosans_anonymous import ParserMonoSans
from .parser_proxyscrape_http import ParserProxyScrapeHttp
from .parser_proxyscrape import ParserProxyScrape
from .parser_proxyspace_socks5 import ParserProxySpaceSocks5
from .parser_socks_proxy import ParserSocksProxy
from .parser_spys_de import ParserSpysDE
from .parser_spys_nl import ParserSpysNL
from .parser_spys_us import ParserSpysUS
from .parser_ssl_proxies import ParserSSLProxies
from .parser_sunny9577_proxy_scraper import ParserSunnyProxyScraper
from .parser_roosterkid_openproxylist_socks4 import ParserRoosterkidOpenproxylistSocks4
from .parser_roosterkid_openproxylist_socks5 import ParserRoosterkidOpenproxylistSocks5
from .parser_murongpig_proxy_master_http import ParserMurongpigProxyMasterHttp
from .parser_murongpig_proxy_master_socks4 import ParserMurongpigProxyMasterSocks4
from .parser_murongpig_proxy_master_socks5 import ParserMurongpigProxyMasterSocks5


proxy_list = [
    {
        'url': 'https://free-proxy-list.net/',
        'parser': ParserFreeProxyList,
    },
    {
        'url': 'https://api.lumiproxy.com/web_v1/free-proxy/list?page_size=1000&page=1&country_code=nl',
        'parser': ParserLumiProxy,
    },
    {
        'url': 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=all&country=NL&anonymity=all&timeout=15000&proxy_format=ipport&format=json',  # noqa: B950
        'parser': ParserProxyScrape,
    },
    {
        'url': 'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt',
        'parser': ParserMonoSans,
    },
    {
        'url': 'https://multiproxy.org/txt_all/proxy.txt',
        'parser': ParserMultiProxy,
    },
    {
        'url': 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=NL&ssl=all&anonymity=all',  # noqa: B950
        'parser': ParserProxyScrapeHttp,
    },
    {
        'url': 'https://socks-proxy.net/',
        'parser': ParserSocksProxy,
    },
    {
        'url': 'https://proxyspace.pro/socks5.txt',
        'parser': ParserProxySpaceSocks5,
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
    {
        'url': 'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json',
        'parser': ParserSunnyProxyScraper,
    },
    {
        'url': 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
        'parser': ParserRoosterkidOpenproxylistSocks4,
    },
    {
        'url': 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
        'parser': ParserRoosterkidOpenproxylistSocks5,
    },
    {
        'url': 'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
        'parser': ParserMurongpigProxyMasterHttp,
    },
    {
        'url': 'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt',
        'parser': ParserMurongpigProxyMasterSocks4,
    },
    {
        'url': 'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt',
        'parser': ParserMurongpigProxyMasterSocks5,
    },
]
