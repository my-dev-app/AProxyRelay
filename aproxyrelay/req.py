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
from ssl import SSLCertVerificationError, SSLError
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ServerDisconnectedError, \
    ClientResponseError, \
    ClientOSError, \
    InvalidURL, \
    ConnectionTimeoutError
from aiohttp_socks import ProxyConnectionError, ProxyConnector, ProxyError
from asyncio import IncompleteReadError, gather, TimeoutError
from json import dumps

from .scrapers import proxy_list


class AProxyRelayRequests(object):
    def __init__(self) -> None:
        """
        Initialize an instance of AProxyRelayRequests.
        """
        self.logger.info("[aProxyRelay] Request module initialized!")

    def _chunk_list(self, lst, chunk_size):
        """Chunks a list in its desired size"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

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

        if hasattr(parser, 'custom_request'):
            response = await parser.custom_request(url=url)
            self.logger.info(f"[aProxyRelay] Scraper: {url}, Status Code: {response.status_code}")
            if response.status_code == 200:
                new_queue = await parser.scrape(parser.zone, response)
                while not new_queue.empty():
                    row = new_queue.get()
                    if self.filter:
                        self._queue_filter.put(row)
                    else:
                        self.proxies.put(row)
        else:
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

    async def _test_all_proxies(self):
        """
        Use asyncio.gather to run multiple requests concurrently by executing `self._test_proxy_link`.
        """
        # Use asyncio.gather to run multiple tests concurrently
        raw = []
        while not self._queue_filter.empty():
            _target = self._queue_filter.get()
            _target['proxy'] = f"{_target['protocol'].replace('https', 'http')}://{_target['ip']}:{_target['port']}"
            raw.append(_target)

        # Remove duplicate entries
        to_filter = [dict(x) for x in list(set([tuple(item.items()) for item in raw]))]
        self.logger.info(f"[aProxyRelay] Found ({int(len(raw)) - int(len(to_filter))}) duplicates which have been removed")
        tasks = [self._test_proxy_link(proxy['proxy'], proxy) for proxy in to_filter]
        # We have to chunk our tasks, otherwise the internet bandwitdh might be compromised
        chunks = self._chunk_list(tasks, 10000)
        i = 0
        for chunk in chunks:
            self.logger.info(f"[aProxyRelay] Brewing ({i}/{len(tasks)}) ... please wait ...")
            i += int(len(chunk))
            # Use asyncio.gather to concurrently execute all tasks
            await gather(*chunk)
        # await gather(*tasks)

    async def _test_proxy_link(self, proxy_url, data) -> None:
        """
        Asynchronously call gg.my-dev.app, a website built by the creator of this package.
        If the connection was successful, the proxy works!

        Executes if `filter` is set to True

        Args:
            proxy_url: The URL of the proxy to be tested.
            data: Additional data for the proxy test.
        """
        # If port is empty, assume port 80
        if data['port'] == '':
            data['port'] = '80'
        # Make sure port is range
        if int(data['port']) < 0 or int(data['port']) > 65535: return
        try:
            self.logger.debug(f'[aProxyRelay] Processing: {proxy_url} -> Added to queue')
            connector = ProxyConnector.from_url(proxy_url.replace('unknown', 'socks4'))
            timeout = ClientTimeout(total=self.timeout, connect=self.timeout)
            async with ClientSession(connector=connector, timeout=timeout) as session:
                async with session.post(
                    'https://gg.my-dev.app/api/v1/proxies/validate/lib',
                    headers={
                        **self._get_header(),
                        'Content-Type': 'application/json'
                    },
                    data=dumps(data)
                ) as response:
                    if response.status == 200:
                        self.proxies.put(data)
                        self._filtered_available = self._filtered_available + 1
                        self.logger.debug(f'[aProxyRelay] Succeed: {proxy_url} -> Freshly Discovered')
                    else:
                        self._filtered_failed = self._filtered_failed + 1
                        self.logger.debug(f'[aProxyRelay] Succeed: {proxy_url} -> Addres Known')
        except (
            ClientOSError,
            InvalidURL,
            ConnectionResetError,
            ProxyError,
            SSLCertVerificationError,
            ProxyConnectionError,
            ConnectionTimeoutError,
            IncompleteReadError,
            UnicodeEncodeError,
            SSLError,
            ConnectionAbortedError,
            ServerDisconnectedError,
            ClientResponseError,
            TimeoutError
        ) as e:
            self.logger.debug(f'[aProxyRelay] Failed: {proxy_url} -> {repr(e)}')
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

    async def _obtain_targets(self, proxy_url, target) -> None:
        """
        Asynchronously fetch the targets with our proxies.
        The 'steam' variable should be defaulted to False and should only be used when targeting Steam.

        Args:
            target: The target URL to be fetched.
            proxy_url: The URL of the proxy to be used for the request.
        """
        try:
            connector = ProxyConnector.from_url(proxy_url.replace('unknown', 'socks4'))
            timeout = ClientTimeout(total=self.timeout, connect=self.timeout)
            async with ClientSession(connector=connector, timeout=timeout) as session:
                async with session.get(
                    target,
                    headers={
                        **self._get_header(),
                        'Content-Type': 'application/json'
                    },
                ) as response:
                    status = response.status
                    if status in (200, 202,):
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
            ClientOSError,
            InvalidURL,
            ConnectionResetError,
            ProxyError,
            SSLCertVerificationError,
            ProxyConnectionError,
            ConnectionTimeoutError,
            IncompleteReadError,
            UnicodeEncodeError,
            SSLError,
            ConnectionAbortedError,
            ServerDisconnectedError,
            ClientResponseError,
            TimeoutError
        ) as e:
            self.logger.debug(f'[aProxyRelay] Failed: {target} -> {repr(e)}')
            self._queue_target_process.put(target)
