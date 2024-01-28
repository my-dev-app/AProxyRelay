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
from queue import Queue

import asyncio
import aiohttp


class AProxyRelayProcessor(object):
    def __init__(self) -> None:
        """
        Initialize an instance of AProxyRelayProcessor.
        """
        self._queue_target_process = Queue()  # holds targets
        self._queue_result = Queue()  # Holds target results

    async def _process_targets_main(self) -> None:
        """
        Start the Proxy Relay Processor. Proxies in the queue are nothing less than burners.
        When they fail, we delete them from memory. Once the proxy queue is empty, we look for new proxies
        before we continue with our targets.
        """
        tasks = []
        while not self._queue_target_process.empty():
            proxy = self.proxies.get()
            if type(proxy) is dict:
                proxy = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"

            target = self._queue_target_process.get()
            # For each parser, fetch the URL related to it
            tasks.append(self._fetch_targets(target, proxy))
            self.proxies.put(proxy)

        # Wait for all requests to complete
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            print(e)

        self.logger.info(f'Processing ({self._queue_target_process.qsize()}) items in Queue ... Please wait...')

        if self.proxies.empty() and self._queue_target_process.qsize() > 0:
            await self.get_proxies()
            await self.process_targets()
        elif not self.proxies.empty() and self._queue_target_process.qsize() > 0:
            await self.process_targets()

    async def _fetch_targets(self, target: str, proxy_url: str) -> None:
        """
        Asynchronously fetch the targets with our proxies.
        The 'steam' variable should be defaulted to False and should only be used when targeting Steam.

        Args:
            target: The target URL to be fetched.
            proxy_url: The URL of the proxy to be used for the request.
        """
        conn = ProxyConnector(remote_resolve=True)

        async with aiohttp.ClientSession(connector=conn, request_class=ProxyClientRequest, conn_timeout=self.timeout) as session:
            try:
                async with session.get(target, proxy=proxy_url, headers=self._get_header()) as response:
                    self.logger.debug(f"Requesting {target} with ({proxy_url}) -> Status Code: {response.status}")
                    if response.status == 200:
                        self.proxies.put(proxy_url)
                        data = await response.json()
                        if self._steam and data[target.split('appids=')[1]]['success']:
                            self._queue_result.put(data[target.split('appids=')[1]]['data'])
                        elif not self._steam:
                            self._queue_result.put(data)
                    else:
                        self._queue_target_process.put(target)
            except Exception as e:
                self.logger.debug(f"Proxy request failed with error: {e}")
                self._queue_target_process.put(target)
