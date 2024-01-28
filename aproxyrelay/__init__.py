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
import asyncio
from datetime import datetime, UTC
from queue import Queue

import logging

from .core import AProxyRelayCore


class AProxyRelay(AProxyRelayCore):
    def __init__(
        self,
        targets: list[str],
        timeout: int = 5,
        test_proxy: bool = True,
        test_timeout: int = 20,
        zone: str = 'us',
        debug: bool = False,
        steam: bool = False
    ) -> None:
        """
        Initialize an instance of AProxyRelay.

        Args:
            targets (list[str]): Target URL's to obtain data from.
            timeout (int): Amount of time in seconds before a connection is cancelled if not succeeded.
            test_proxy (bool): When True, test proxy connections before utilizing them.
            test_timeout (int): Timeout for testing proxy connections in seconds.
            zone (str): Zone identifier, e.g., 'us', 'nl', 'de', 'uk', etc etc.
            debug (bool): Enable debug mode if True.
            steam (bool): Enable Steam mode if True.
        """
        # Configure the logger
        logging.basicConfig(level=logging.INFO if not debug else logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # TODO raise exceptions
        self.timeout = timeout
        self.test_timeout = test_timeout
        self.test_proxy = test_proxy
        self.zone = zone
        self.debug = debug

        self._steam = steam

        AProxyRelayCore.__init__(self)
        for item in list(set(targets)):
            self._queue_target_process.put(item)

    async def _main(self) -> Queue:
        """
        Start the scrape task asynchronously. Once finished, you will end up with the data from the API in a Queue.

        Returns:
            Queue: A queue containing the scraped data from the API.
        """
        await self.get_proxies()
        await self.process_targets()
        return self._queue_result

    def start(self) -> Queue:
        """
        Start asynchronous scraping and return the results in a List format.

        Returns:
            Queue: A queue containing the scraped data from the API.
        """
        started = datetime.now(UTC)
        self.logger.info(f'Started proxy relay at {started} ... Please wait ...!')

        loop = asyncio.get_event_loop()
        loop.set_debug(self.debug)

        # Create a task and set its name
        task = loop.create_task(self._main())
        task.set_name("AProxyRelay")

        loop.run_until_complete(task)
        self.logger.info(f'Data scraped! Took {datetime.now(UTC) - started}, enjoy!')
        return task.result()
