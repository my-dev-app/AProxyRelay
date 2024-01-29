from setuptools import setup, find_packages

import os

# Retrieve the version from the environment variable or use a default value
version = os.getenv('CUSTOM_VERSION', '1.0.0')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aproxyrelay',
    version=version,
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'aiosocks2',
        'beautifulsoup4',
    ],
    extras_require={
        'dev': [
            'build',
            'flake8-bugbear',
            'pytest',
            'pytest-cov',
            'pytest-sugar',
            'pytest-xdist',
            'setuptools',
            'twine',
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
    long_description_content_type='text/markdown',
    url='https://github.com/my-dev-app/proxy-relay',
    license='GNU AGPLv3',
)
