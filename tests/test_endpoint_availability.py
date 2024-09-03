import pytest
import requests

from aproxyrelay.agents import UserAgents
from aproxyrelay.scrapers import proxy_list


def is_website_reachable(url, agent):
    headers = {
        'User-Agent': agent,
    }
    try:
        response = requests.get(url, timeout=5, headers=headers)
        if response.status_code in (200, 202,):
            return response
        return False
    except requests.exceptions.RequestException:
        return False


@pytest.mark.asyncio
async def test_parse_proxy_data():
    agents = UserAgents()
    for endpoint in proxy_list:
        url = endpoint.get("url")
        if not url:
            pytest.fail(f"Endpoint is missing 'url' key: {endpoint}")

        parser = endpoint.get("parser")
        if not parser:
            pytest.fail(f"Parser for endpoint is required key: {endpoint}")

        url = await parser.format_url(url)

        # Check if the website is reachable without mocking (real test)
        if not is_website_reachable(url, agents.random()):
            pytest.fail(f"Website {url} is not reachable, cannot proceed with scraping.")

        # You would continue your scraping logic here if the site is reachable
        print(f"Website {url} is reachable, proceeding with tests.")
