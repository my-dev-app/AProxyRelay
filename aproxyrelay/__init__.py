# -*- mode: python ; coding: utf-8 -*-
"""
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
-------------------------------------
An async request library which requests data by utilizing various proxy servers.
Automatically rotates bad proxy servers, preserves data which failed to request.
Makes scraping API's easy and fun.
"""
import asyncio

from .core import AProxyRelayCore


class AProxyRelay(object):
    def __init__(self, targets: list[str], timeout: int = 5, test_proxy: bool = True) -> None:
        """
        Args:
            targets list[str]: Target URL's to obtain data from
            timeout int: amount of time in seconds before a connection is cancelled if not succeeded
            test_proxy bool: When True, test proxy connections before utilizing them
        """
        self._core = AProxyRelayCore(timeout=timeout, test_proxy=test_proxy)
        self.proxies = []

    async def _main(self) -> list:
        """
        Starts Proxy task, returns list of results
        """
        # Obtain proxies
        await self._core._obtain_proxies()
        # set proxy list
        self.proxies = self._core._queue_result
        return self.proxies

    def start(self) -> list:
        """
        Start asynchronious scraping, returns results in Array format
        """
        loop = asyncio.get_event_loop()
        loop.set_debug(True)

        # Create a task and set its name
        task = loop.create_task(self._main())
        task.set_name("AProxyRelay")

        loop.run_until_complete(task)
        return task.result()
