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
from asyncio import gather
from queue import Queue


class AProxyRelayProcessor(object):
    def __init__(self) -> None:
        """
        Initialize an instance of AProxyRelayProcessor.
        """
        self._queue_result = Queue()  # Holds target results

    def _chunk_list(self, lst, chunk_size):
        """Chunks a list in its desired size"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    async def _process_targets_main(self) -> None:
        """
        Start the Proxy Relay Processor. Proxies in the queue are nothing less than burners.
        When they fail, we delete them from memory. Once the proxy queue is empty, we look for new proxies
        before we continue with our targets.
        """
        self.logger.info('[aProxyRelay] Processing ...')

        tasks = []

        while not self._queue_target_process.empty():
            proxy = self.proxies.get()
            if isinstance(proxy, dict):
                proxy = f"{proxy['protocol'].replace('https', 'http')}://{proxy['ip']}:{proxy['port']}"
            target = self._queue_target_process.get()

            # Append the coroutine object to the tasks list
            tasks.append(self._obtain_targets(proxy, target))

        # We have to chunk our tasks, otherwise the internet bandwitdh might be compromised
        chunks = self._chunk_list(tasks, 10000)
        i = 0
        for chunk in chunks:
            self.logger.info(f"[aProxyRelay] Processing ({i}/{len(tasks)}) ... please wait ...")
            i += int(len(chunk))
            # Use asyncio.gather to concurrently execute all tasks
            await gather(*chunk)
        # # Use asyncio.gather to concurrently execute all tasks
        # await gather(*tasks)

        self.logger.info(f'[aProxyRelay] Processing ({self._queue_target_process.qsize()}) items in Queue using ({self.proxies.qsize()}) proxies ... Please wait...')  # noqa: B950

        # Proxy queue is empty but targets are available
        if self.proxies.empty() and self._queue_target_process.qsize() > 0:
            self.logger.info(
                f'[aProxyRelay] All Proxies exhausted ({self._queue_target_process.qsize()}) items left in Queue ... Please wait...'
            )
            await self.get_proxies()
            await self.process_targets()
        # Proxy queue has proxies targets are available
        elif not self.proxies.empty() and self._queue_target_process.qsize() > 0:
            await self.process_targets()
