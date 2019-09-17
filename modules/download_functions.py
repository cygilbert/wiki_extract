"""
Download functions
"""

import requests
from bs4 import BeautifulSoup


def get_wikidump_url(base_url="https://dumps.wikimedia.org/enwiki/"):
    index = requests.get(base_url).text
    # get the latest version of the dump
    soup_index = BeautifulSoup(index, 'html.parser')
    dumps_list = [
        a['href'] for a in soup_index.find_all('a')
        if a.has_attr('href')
    ]
    return base_url + dumps_list[-2]


def get_list_url_wikidump(
        dump_url="https://dumps.wikimedia.org/enwiki/20190901/"
        ):
    return [True]
