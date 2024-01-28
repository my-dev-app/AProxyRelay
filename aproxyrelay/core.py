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
from aiosocks2.connector import ProxyConnector, ProxyClientRequest
from datetime import datetime, UTC
from queue import Queue

import asyncio
import aiohttp
import json


from .agents import UserAgents
from .scrapers import proxy_list
from .process import AProxyRelayProcessor


class AProxyRelayCore(AProxyRelayProcessor):
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

        # Various queues which hold processing steps.
        self._queue_scrape_urls = Queue()
        self._queue_to_validate = Queue()

        self._queue_target_process = Queue()  # holds targets
        self._queue_result = Queue()  # Holds target results

        self.proxies = Queue()
        AProxyRelayProcessor.__init__(self)

    async def get_proxies(self) -> None:
        """
        Asynchronously fill the self.proxies queue with fresh proxies.
        """
        await self._process()

    async def process_targets(self) -> None:
        """
        Asynchronously process targets with available proxies.
        """
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

    async def _process(self) -> None:
        """
        Asynchronously process the library.
        """
        started = datetime.now(UTC)
        for item in proxy_list:
            self._queue_scrape_urls.put(item['url'])

        # For each parser, fetch the URL related to it
        task_request_proxy_list = []
        while not self._queue_scrape_urls.empty():
            url = self._queue_scrape_urls.get()
            task_request_proxy_list.append(self._request_scraper_page(url))

        # Wait for all requests to complete
        await asyncio.gather(*task_request_proxy_list)

        if self.test_proxy:
            await self._test_proxies()

        self.logger.info(f'Found {self.proxies.qsize()} working proxies, took {datetime.now(UTC) - started}, Please wait...')

    async def _request_scraper_page(self, url) -> None:
        """
        Asynchronously fetch a URL and execute the pre-coded scraper for that specific website.

        Args:
            url: The URL to be fetched and processed.
        """
        async with aiohttp.ClientSession(conn_timeout=self.timeout) as session:
            # try:
            # Make your asynchronous request here
            parser = [p for p in proxy_list if p['url'] == url][0]['parser']
            target_url = await parser.format_url(url, self.zone)
            async with session.get(target_url, headers=self._get_header()) as response:
                # Process the response as needed
                self.logger.debug(f"URL: {await parser.format_url(url, zone=self.zone)}, Status Code: {response.status}")
                if response.status == 200:
                    new_queue = await parser.scrape(self.zone, response)
                    while not new_queue.empty():
                        row = new_queue.get()
                        if self.test_proxy:
                            self._queue_to_validate.put(row)
                        else:
                            self.proxies.put(row)
            # except Exception as e:
            #     self.logger.info(f"Request for URL {url} failed with error: {e}")

    async def _test_proxies(self) -> None:
        """
        Asynchronously test all scraped proxies. Working proxies will be put into the 'results' variable of the core.
        """
        # Create a list to hold the tasks for making asynchronous requests
        tasks = []

        while not self._queue_to_validate.empty():
            data = self._queue_to_validate.get()
            port = str(data["port"])
            ip = f"{data['protocol'].replace('https', 'http')}://{data['ip']}{f':{port}' if len(str(port)) > 0 else ''}"
            tasks.append(self._test_proxy_link(ip, data))

        # Wait for all requests to complete
        await asyncio.gather(*tasks)

    async def _test_proxy_link(self, proxy_url, data) -> None:
        """
        Asynchronously call gg.my-dev.app, a website built by the creator of this package.
        If the connection was successful, the proxy works!

        Args:
            proxy_url: The URL of the proxy to be tested.
            data: Additional data for the proxy test.
        """
        conn = ProxyConnector(remote_resolve=True)

        async with aiohttp.ClientSession(
            connector=conn,
            request_class=ProxyClientRequest,
            conn_timeout=self.test_timeout
        ) as session:
            try:
                async with session.post(
                    'https://gg.my-dev.app/api/v1/proxies/validate/lib',
                    proxy=proxy_url,
                    headers={
                        **self._get_header(),
                        'Content-Type': 'application/json'
                    },
                    data=json.dumps(data)
                ) as response:
                    self.logger.debug(f"Proxy usage -> Status Code: {response.status}")
                    if response.status == 200:
                        self.proxies.put(data)
            except Exception as e:
                self.logger.debug(f"Proxy request failed with error: {e}")
