# -*- mode: python ; coding: utf-8 -*-
"""
░░      ░░       ░░       ░░░      ░░  ░░░░  ░  ░░░░  ░       ░░        ░  ░░░░░░░░      ░░  ░░░░  ░
▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒▒  ▒▒  ▒▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒
▓  ▓▓▓▓  ▓       ▓▓       ▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓▓▓    ▓▓▓       ▓▓      ▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓
█        █  ███████  ███  ██  ████  ██  ██  █████  ████  ███  ██  ███████  ███████        ████  ████
█  ████  █  ███████  ████  ██      ██  ████  ████  ████  ████  █        █        █  ████  ████  ████
By undeƒined
------------

Core of the proxy relay, contains async within the library
"""
from aiohttp import ClientSession
from datetime import datetime, UTC
from queue import Queue

from .agents import UserAgents
from .scrapers import proxy_list
from .process import AProxyRelayProcessor
from .req import AProxyRelayRequests


class AProxyRelayCore(AProxyRelayProcessor, AProxyRelayRequests):
    """
    Core class that manages proxies and scraped links.
    Designed for speed and to bypass API limiters.
    """
    def __init__(self) -> None:
        """
        Initialize an instance of AProxyRelayCore.
        """
        # Initialize class for user agents
        # User agents are important for tricking connections we are requesting from different devices
        self._agents = UserAgents()

        # Filter
        self._queue_filter = Queue()  # Proxies about to get filtered on availability
        self._filtered_failed = 0
        self._filtered_available = 0
        self._filtered_ggs = 0

        self._queue_result = Queue()  # Holds target results

        self.proxies = Queue()
        AProxyRelayProcessor.__init__(self)
        AProxyRelayRequests.__init__(self)

    async def _reset_numbers(self):
        self._filtered_failed = 0
        self._filtered_available = 0
        self._filtered_ggs = 0

    async def get_proxies(self) -> None:
        """
        Asynchronously fill the self.proxies queue with fresh proxies.
        """
        self.logger.info('[aProxyRelay] Initializing parsers ...')
        ggs = []
        scrapes = []
        for item in proxy_list:
            self.logger.info(f'[aProxyRelay] Loading: {item["parser"].__name__}')
            parser = item['parser']
            for zone in self.zones:
                url = await parser.format_url(url=item['url'], zone=zone)
                if url.startswith('https://gg.my-dev.app/'):
                    ggs.append(url)
                else:
                    scrapes.append(url)
        ggs = list(set(ggs))
        scrapes = list(set(scrapes))
        self.logger.info(f'[aProxyRelay] Parsers loaded: GG: {len(ggs)}, Other: {len(scrapes)}, Total: {len(ggs + scrapes)} ...')

        if self.scrape:
            async with ClientSession(conn_timeout=self.timeout) as session:
                await self._fetch_proxy_page(scrapes, session)
            self.logger.info(f'[aProxyRelay] Scraper: Found {self._queue_filter.qsize()} competent proxy servers')
        else:
            self.logger.info('[aProxyRelay] Scraper: Skip discovery of new proxy servers ...')

        if self.filter and self.scrape:
            self.logger.info(f'[aProxyRelay] Validating: Proxies ({self._queue_filter.qsize()}), checking if proxies meet connection requirements ...')  # noqa: B950
            async with ClientSession(conn_timeout=15) as session:
                await self._test_all_proxies(session)
            self.logger.info(f'[aProxyRelay] Filter: Found {self._filtered_failed} incompetent and {self._filtered_available} available proxy servers in {datetime.now(UTC) - self.started}')  # noqa: B950
        else:
            while not self._queue_filter.empty():
                _target = self._queue_filter.get()
                _target['proxy'] = f"{_target['protocol'].replace('https', 'http')}://{_target['ip']}:{_target['port']}"
                self.proxies.put(_target)
            self.logger.info('[aProxyRelay] Filter: Skip tests for scraped proxy servers ...')

        async with ClientSession(conn_timeout=self.timeout) as session:
            await self._fetch_proxy_servers(ggs, session)

        self.logger.info(f'[aProxyRelay] Scraper: Found {self._filtered_ggs} additional available proxy servers')
        self.logger.info(f'[aProxyRelay] Found {self.proxies.qsize()} working proxies, took {datetime.now(UTC) - self.started}, Please wait...')  # noqa: B950

    async def process_targets(self) -> None:
        """
        Asynchronously process targets with available proxies.
        """
        await self._reset_numbers()
        await self._process_targets_main()

    def _get_header(self) -> dict:
        """
        Obtain a random user-agent header.

        Returns:
            dict: A dictionary containing the user-agent header.
        """
        return {
            'User-Agent': self._agents.random()
        }
