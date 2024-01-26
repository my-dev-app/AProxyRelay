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

import logging

from .core import AProxyRelayCore


class AProxyRelay(AProxyRelayCore):
    def __init__(self, targets: list[str], timeout: int = 5, test_proxy: bool = True, zone: str = 'us', debug: bool = False, steam: bool = False) -> None:
        """
        Args:
            targets list[str]: Target URL's to obtain data from
            timeout int: amount of time in seconds before a connection is cancelled if not succeeded
            test_proxy bool: When True, test proxy connections before utilizing them
        """
        # Configure the logger
        logging.basicConfig(level=logging.INFO if not debug else logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # TODO raise exceptions
        self.timeout = timeout
        self.test_proxy = test_proxy
        self.zone = zone
        self.debug = debug

        self._steam = steam

        AProxyRelayCore.__init__(self)
        for item in targets:
            self._queue_target_process.put(item)

    async def _main(self) -> list:
        """
        Starts scrape task, once finised, you will endup with the data from the api in an array.
        """
        await self.get_proxies()
        await self.process_targets()
        return self._queue_result

    def start(self) -> list:
        """
        Start asynchronious scraping, returns results in Array format
        """
        started = datetime.now(UTC)
        loop = asyncio.get_event_loop()
        loop.set_debug(self.debug)

        # Create a task and set its name
        task = loop.create_task(self._main())
        task.set_name("AProxyRelay")

        loop.run_until_complete(task)
        self.logger.info(f'Data scraped in {datetime.now(UTC) - started}')
        return task.result()
