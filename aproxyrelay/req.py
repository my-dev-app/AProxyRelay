# -*- mode: python ; coding: utf-8 -*-
"""
░░      ░░       ░░       ░░░      ░░  ░░░░  ░  ░░░░  ░       ░░        ░  ░░░░░░░░      ░░  ░░░░  ░
▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒▒  ▒▒  ▒▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒
▓  ▓▓▓▓  ▓       ▓▓       ▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓▓▓    ▓▓▓       ▓▓      ▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓
█        █  ███████  ███  ██  ████  ██  ██  █████  ████  ███  ██  ███████  ███████        ████  ████
█  ████  █  ███████  ████  ██      ██  ████  ████  ████  ████  █        █        █  ████  ████  ████
By undeƒined
------------

Class which handles all requests made throughout the library.
"""
from aiohttp.client_exceptions import ClientHttpProxyError, \
    ServerDisconnectedError, \
    ClientProxyConnectionError, \
    ClientResponseError, \
    ClientOSError, \
    ServerTimeoutError, \
    InvalidURL
from aiosocks2.errors import SocksError
from asyncio import gather, TimeoutError
from json import dumps

from .scrapers import proxy_list


class AProxyRelayRequests(object):
    def __init__(self) -> None:
        """
        Initialize an instance of AProxyRelayRequests.
        """
        self.logger.info("[aProxyRelay] Request module initialized!")

    async def _fetch_proxy_page(self, urls, session):
        """
        Use asyncio.gather to run multiple requests concurrently by executing `self._request_proxy_page`.
        Is executed when `scrape` is set to True

        Args:
            urls (list[str]): Target urls to fetch
            session: aiohttp session without proxy support
        """
        tasks = [self._request_proxy_page(url, session) for url in urls]
        await gather(*tasks)

    async def _request_proxy_page(self, url, session) -> None:
        """
        Asynchronously fetch a URL and execute the pre-coded scraper for that specific website.

        Args:
            url (str): The URL to be fetched and processed.
            session: aiohttp session without proxy support
        """
        if parsers := [p for p in proxy_list if p['url'] == url]:
            parser = parsers[0]['parser']
        else:
            return

        async with session.get(url, headers=self._get_header()) as response:
            self.logger.info(f"[aProxyRelay] Scraper: {url}, Status Code: {response.status}")
            if response.status == 200:
                new_queue = await parser.scrape(parser.zone, response)
                while not new_queue.empty():
                    row = new_queue.get()
                    if self.filter:
                        self._queue_filter.put(row)
                    else:
                        self.proxies.put(row)

    async def _test_all_proxies(self, session):
        """
        Use asyncio.gather to run multiple requests concurrently by executing `self._test_proxy_link`.

        Args:
            session: aiohttp session without proxy support
        """
        # Use asyncio.gather to run multiple tests concurrently
        to_filter = []
        while not self._queue_filter.empty():
            _target = self._queue_filter.get()
            _target['proxy'] = f"{_target['protocol'].replace('https', 'http')}://{_target['ip']}:{_target['port']}"
            to_filter.append(_target)

        # Remove duplicate entries
        to_filter = [dict(x) for x in list(set([tuple(item.items()) for item in to_filter]))]
        tasks = [self._test_proxy_link(proxy['proxy'], proxy, session) for proxy in to_filter]
        await gather(*tasks)

    async def _test_proxy_link(self, proxy_url, data, session) -> None:
        """
        Asynchronously call gg.my-dev.app, a website built by the creator of this package.
        If the connection was successful, the proxy works!

        Executes if `filter` is set to True

        Args:
            proxy_url: The URL of the proxy to be tested.
            data: Additional data for the proxy test.
        """
        try:
            async with session.post(
                'https://gg.my-dev.app/api/v1/proxies/validate/lib',
                proxy=proxy_url,
                headers={
                    **self._get_header(),
                    'Content-Type': 'application/json'
                },
                data=dumps(data)
            ) as response:
                if response.status == 200:
                    self.proxies.put(data)
                    self._filtered_available = self._filtered_available + 1
                else:
                    self._filtered_failed = self._filtered_failed + 1
        except (
            ClientHttpProxyError,
            ServerDisconnectedError,
            ClientProxyConnectionError,
            ClientResponseError,
            ClientOSError,
            ServerTimeoutError,
            InvalidURL,
        ):
            self._filtered_failed = self._filtered_failed + 1

    async def _fetch_proxy_servers(self, urls, session):
        """
        Use asyncio.gather to run multiple requests concurrently by executing `self._request_proxy_servers`.
        Always executes. The targets in `urls` are gg.my-dev.app endpoints.

        Args:
            urls (list[str]): List of urls starting with 'https://gg.my-dev.app'
            session: aiohttp session without proxy support
        """
        # Use asyncio.gather to run multiple requests concurrently
        tasks = [self._request_proxy_servers(url, session) for url in urls]
        await gather(*tasks)

    async def _request_proxy_servers(self, url, session) -> None:
        """
        Asynchronously fetch a URL and execute the pre-coded scraper for that specific website.

        Args:
            url: The URL to be fetched and processed.
        """
        if parsers := [p for p in proxy_list if p['url'].startswith('https://gg.my-dev.app')]:
            parser = parsers[0]['parser']
        else:
            return

        zone = url.split('zone=')[1].split('&')[0]

        async with session.get(url, headers=self._get_header()) as response:
            self.logger.info(f"[aProxyRelay] Scraper: {url}, Status Code: {response.status}")
            if response.status == 200:
                new_queue = await parser.scrape(zone, response)
                while not new_queue.empty():
                    row = new_queue.get()
                    self.proxies.put(row)
                    self._filtered_ggs = self._filtered_ggs + 1

    async def _obtain_targets(self, proxy_url, target, session) -> None:
        """
        Asynchronously fetch the targets with our proxies.
        The 'steam' variable should be defaulted to False and should only be used when targeting Steam.

        Args:
            target: The target URL to be fetched.
            proxy_url: The URL of the proxy to be used for the request.
        """
        try:
            async with session.get(
                target,
                proxy=proxy_url,
                headers={
                    **self._get_header(),
                    'Content-Type': 'application/json'
                },
            ) as response:
                status = response.status
                if status == 200:
                    self.proxies.put(proxy_url)
                    data = await response.json()
                    if data:
                        if pack := self.unpack(data, target):
                            self._queue_result.put(pack)
                        else:
                            self.logger.warning(f'[aProxyRelay] Could not unpack data for: {target}')
                    else:
                        self.logger.warning(f'[aProxyRelay] Target {target} Data seems to be None: {data}')
                else:
                    self._queue_target_process.put(target)

        except (
            ClientHttpProxyError,
            ServerDisconnectedError,
            ClientProxyConnectionError,
            ClientResponseError,
            ClientOSError,
            ServerTimeoutError,
            InvalidURL,
            SocksError,
            TimeoutError,
        ):
            self._queue_target_process.put(target)
