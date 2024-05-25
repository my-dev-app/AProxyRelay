# -*- mode: python ; coding: utf-8 -*-
"""
░░      ░░       ░░       ░░░      ░░  ░░░░  ░  ░░░░  ░       ░░        ░  ░░░░░░░░      ░░  ░░░░  ░
▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒▒  ▒▒  ▒▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒
▓  ▓▓▓▓  ▓       ▓▓       ▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓▓▓    ▓▓▓       ▓▓      ▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓
█        █  ███████  ███  ██  ████  ██  ██  █████  ████  ███  ██  ███████  ███████        ████  ████
█  ████  █  ███████  ████  ██      ██  ████  ████  ████  ████  █        █        █  ████  ████  ████
By undeƒined
------------

Process class, once all proxies have been received, we are going to obtain the data for the targets.
This class contains the core mechanics for scraping the targets.
"""
from aiosocks2.connector import ProxyConnector, ProxyClientRequest
from aiohttp import ClientSession
from asyncio import gather
from queue import Queue


class AProxyRelayProcessor(object):
    def __init__(self) -> None:
        """
        Initialize an instance of AProxyRelayProcessor.
        """
        self._queue_result = Queue()  # Holds target results

    async def _process_targets_main(self) -> None:
        """
        Start the Proxy Relay Processor. Proxies in the queue are nothing less than burners.
        When they fail, we delete them from memory. Once the proxy queue is empty, we look for new proxies
        before we continue with our targets.
        """
        self.logger.info('[aProxyRelay] Processing ...')

        async with ClientSession(
            connector=ProxyConnector(remote_resolve=True),
            request_class=ProxyClientRequest,
            conn_timeout=self.timeout
        ) as session:
            tasks = []

            while not self._queue_target_process.empty():
                proxy = self.proxies.get()
                if isinstance(proxy, dict):
                    proxy = f"{proxy['protocol'].replace('https', 'http')}://{proxy['ip']}:{proxy['port']}"
                target = self._queue_target_process.get()

                # Append the coroutine object to the tasks list
                tasks.append(self._obtain_targets(proxy, target, session))
                self.proxies.put(proxy)

            self.proxies = Queue()
            # Use asyncio.gather to concurrently execute all tasks
            await gather(*tasks)

        self.logger.info(f'[aProxyRelay] Processing ({self._queue_target_process.qsize()}) items in Queue ... Please wait...')

        if self.proxies.empty() and self._queue_target_process.qsize() > 0:
            await self.get_proxies()
            await self.process_targets()
        elif not self.proxies.empty() and self._queue_target_process.qsize() > 0:
            await self.process_targets()
