# -*- mode: python ; coding: utf-8 -*-
"""
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
-------------------------------------
Core of the proxy relay, contains async within the library
"""
from queue import Queue

import asyncio
import aiohttp

from aiosocks2.connector import ProxyConnector, ProxyClientRequest
from .sources import _proxy_list


class AProxyRelayCore(object):
    """Core is responsible for obtaining available proxy servers"""
    def __init__(self, timeout: int, test_proxy: bool) -> None:
        self.timeout = timeout
        self.test_proxy = test_proxy

        self._queue_proxy_lists = Queue()
        self._queue_parser = Queue()
        self._queue_to_validate = Queue()
        self._queue_result = Queue()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    async def _prep_proxy_list(self):
        """
        Prepares proxy list queue, fills it with available targets which have parsers.
        """
        for item in _proxy_list:
            self._queue_proxy_lists.put(item['url'])

    async def _obtain_proxies(self):
        """
        Main method of the core class. Fills _queue_result with proxies ready for use.
        """
        # try:
        print('Async method start')
        await self._prep_proxy_list()

        # Create a list to hold the tasks for making asynchronous requests
        tasks = []

        while not self._queue_proxy_lists.empty():
            url = self._queue_proxy_lists.get()
            tasks.append(self._make_async_request(url))
        
        # Wait for all requests to complete
        await asyncio.gather(*tasks)

        await self._process_result()
        if self.test_proxy:
            await self._test_proxies()

        print("Async method end")

        # except Exception as e:
        #     print(f"Async method failed with error: {e}")

    async def _make_async_request(self, url):
        """
        Fetch proxy lists and execute their scrapers
        """
        async with aiohttp.ClientSession(conn_timeout=self.timeout) as session:
            # try:
            # Make your asynchronous request here
            async with session.get(url, headers=self.headers) as response:
                # Process the response as needed
                print(f"URL: {url}, Status Code: {response.status}")
                if response.status == 200:
                    if response.content_type == 'application/json':
                        data = await response.json()
                    elif response.content_type == 'text/html':
                        data = await [p for p in _proxy_list if p['url'] == url][0]['parser']._scrape(response)
                    else:
                        raise ReferenceError(f'None exiting content type for parser: {response.content_type}')
                    await self._prep_parser(url, data)
            # except Exception as e:
            #     print(f"Request for URL {url} failed with error: {e}")
    
    async def _prep_parser(self, url, data):
        """Prepare parser queue with data from various scape providers, filters objects for the parser so the parser
        always obtains a dictionary"""
        if type(data) == list:
            for item in data:
                self._queue_parser.put((url, item, ))
        else:
            self._queue_parser.put((url, data, ))

    async def _prep_result(self, data):
        """Prepare results with data from various scape providers"""
        if type(data) == list:
            for item in data:
                if self.test_proxy:
                    self._queue_to_validate.put(item)
                else:
                    self._queue_result.put(item['ip'])
        else:
            if self.test_proxy:
                self._queue_to_validate.put(data)
            else:
                self._queue_result.put(item['ip'])

    async def _process_result(self):
        """Process any data into a useable result array which returns after promise has been completed"""
        # Create a list to hold the tasks for making asynchronous requests
        tasks = []

        # Process each item in the parser queue, and execute the parser class for that link
        while not self._queue_parser.empty():
            url, data = self._queue_parser.get()
            parser = [p for p in _proxy_list if p['url'] == url][0]['parser'](data=data)
            data = self._prep_result(data=await parser._parse())
            tasks.append(data)

        # Wait for all parsers to complete
        await asyncio.gather(*tasks)

    async def _test_proxies(self):
        """Test all scraped proxies, working proxies will be put into the results variable of the core"""
        # Create a list to hold the tasks for making asynchronous requests
        tasks = []

        while not self._queue_to_validate.empty():
            url = self._queue_to_validate.get()
            tasks.append(self._test_proxy_link(url['ip']))

        # Wait for all requests to complete
        await asyncio.gather(*tasks)

    async def _test_proxy_link(self, proxy_url):
        """Calls gg.my-dev.app, website build by the creator of this package. If the connection was successful, the proxy works!"""
        conn = ProxyConnector(remote_resolve=True)

        async with aiohttp.ClientSession(connector=conn, request_class=ProxyClientRequest, conn_timeout=self.timeout) as session:
            try:
                async with session.get('https://gg.my-dev.app/api/v1/steam/filter/genres/', proxy=proxy_url, headers=self.headers) as response:
                    print(f"Proxy usage -> Status Code: {response.status}")
                    if response.status == 200:
                        self._queue_result.put(proxy_url)
            except Exception as e:
                print(f"Proxy request failed with error: {e}")
