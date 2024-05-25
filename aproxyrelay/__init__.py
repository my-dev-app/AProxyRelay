# -*- mode: python ; coding: utf-8 -*-
"""
░░      ░░       ░░       ░░░      ░░  ░░░░  ░  ░░░░  ░       ░░        ░  ░░░░░░░░      ░░  ░░░░  ░
▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒▒  ▒▒  ▒▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒
▓  ▓▓▓▓  ▓       ▓▓       ▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓▓▓    ▓▓▓       ▓▓      ▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓
█        █  ███████  ███  ██  ████  ██  ██  █████  ████  ███  ██  ███████  ███████        ████  ████
█  ████  █  ███████  ████  ██      ██  ████  ████  ████  ████  █        █        █  ████  ████  ████
By undeƒined
------------

An async request library which requests data by utilizing various proxy servers.
Automatically rotates bad proxy servers, preserves data which failed to request.
Makes scraping API's easy and fun.
"""
from asyncio import get_event_loop, gather
from datetime import datetime, UTC
from logging import basicConfig, INFO, DEBUG, getLogger
from typing import Callable
from queue import Queue

from .core import AProxyRelayCore


class AProxyRelay(AProxyRelayCore):
    def __init__(
        self,
        targets: list[str],
        timeout: int = 5,
        scrape: bool = True,
        filter: bool = True,
        zones: list[str] = ['US'],  # noqa: B006
        unpack: Callable = lambda data, target: data,
        debug: bool = False,
    ) -> None:
        """
        Initialize an instance of AProxyRelay.

        Args:
            targets: list[str]: Target URL's to obtain data from.
            timeout: int: Amount of time in seconds before a connection is cancelled if not succeeded.
            scrape: bool: When True, scrape for proxies (Slow). Otherwise fetch them from one source (Fast).
            filter: bool: When True, test proxy connections before utilizing them.
            zone: list[str]: List of whitelisted proxy zones. Only use proxies located in the provided array.
            unpack: Callable: Filter extracted data through an anonymous method.
            debug: bool: When True, ouput debug logs to terminal.

        Example:
            ```py
                proxy_relay = AProxyRelay(
                    targets=targets,
                    timeout=5,
                    scrape=True,
                    filter=True,
                    zones=['US', 'DE'],
                    unpack=lambda data, target: data[target.split('appids=')[1]]['success'],
                    debug=True,
                )
            ```
        """
        # Configure the logger
        basicConfig(level=INFO if not debug else DEBUG)
        self.logger = getLogger(__name__)

        # Initialize Core
        AProxyRelayCore.__init__(self)

        # TODO raise exceptions for class arguments
        self._queue_target_process = Queue(maxsize=len(targets))
        for item in list(set(targets)):
            self._queue_target_process.put(item)

        self.timeout = timeout
        self.scrape = scrape
        self.filter = filter
        self.zones = [z.upper() for z in zones]
        self.unpack = unpack
        self.debug = debug
        self.started = None

    async def _main(self) -> Queue:
        """
        Start the scrape task asynchronously. Once finished, you will end up with the data from the API in a Queue.

        Returns:
            Queue: A queue containing the scraped data from the API.
        """
        await self.get_proxies()
        if self.proxies.qsize() > 0:
            await self.process_targets()
        else:
            self.logger.error('[aProxyRelay] Could not establish any available proxy! Please try again later.')
        return self._queue_result

    def start(self) -> Queue:
        """
        Start asynchronous scraping and return the results in a List format.

        Returns:
            Queue: A queue containing the scraped data from the API.
        """
        self.started = datetime.now(UTC)
        self.logger.info(f'[aProxyRelay] Started proxy relay at {self.started} ... Please wait ...!')

        loop = get_event_loop()
        loop.set_debug(self.debug)
        results = loop.run_until_complete(gather(self._main()))
        result = results.pop()

        self.logger.info(f'[aProxyRelay] Data scraped! Took {datetime.now(UTC) - self.started}, enjoy!')

        return result
