from setuptools import setup, find_packages


setup(
    name='aproxyrelay',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'aiosocks2',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'myproject-cli = myproject.module1:main',
        ],
    },
    author='undeƒined',
    author_email='my-dev.app@domainsbyproxy.com',
    description='A Proxy Relay, forwarding requests through different IP.',
    url='https://github.com/my-dev-app/proxy-relay',
    license='GNU AGPLv3',
)
