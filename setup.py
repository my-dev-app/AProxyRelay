from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aproxyrelay',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'aiosocks2',
        'beautifulsoup4',
    ],
    extras_require={
        'dev': [
            'flake8-bugbear',
            'pytest',
            'pytest-cov',
            'pytest-django',
            'pytest-sugar',
            'pytest-xdist',
            'setuptools',
            'wheel',
        ],
    },
    entry_points={
        'console_scripts': [
            'myproject-cli = myproject.module1:main',
        ],
    },
    author='undeƒined',
    author_email='my-dev.app@domainsbyproxy.com',
    description='A Proxy Relay, forwarding requests through different IP.',
    long_description=long_description,
    url='https://github.com/my-dev-app/proxy-relay',
    license='GNU AGPLv3',
)
