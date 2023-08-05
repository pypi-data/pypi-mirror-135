from setuptools import setup

setup(
    name='lostify',
    version='1.0.6',
    description='A Spotify API wrapper dedicated to people with a brain',
    author=".()#1030",
    url='https://wock.club',
    download_url='https://github.com/qcki/lostify/archive/refs/tags/Beta.tar.gz',
    install_requires=[
        'aiohttp>=3.6.0,<3.9.0'
    ],
    packages=['lostify']
)