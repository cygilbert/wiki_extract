"""
Download functions
"""

import requests
from bs4 import BeautifulSoup


def get_soup_from_url(url="https://en.wikipedia.org/wiki/English_Wikipedia"):
    index = requests.get(url).text
    return BeautifulSoup(index, 'html.parser')


def get_wikidump_url(base_url="https://dumps.wikimedia.org/enwiki/"):
    soup_index = get_soup_from_url(base_url)
    dumps_list = [
        a['href'] for a in soup_index.find_all('a')
        if a.has_attr('href')
    ]
    return base_url + dumps_list[-2]


def get_list_downloads_wikidump(
        dump_url="https://dumps.wikimedia.org/enwiki/20190901/"
        ):
    soup_dump = get_soup_from_url(dump_url)
    files = []
    for file in soup_dump.find_all('li', {'class': 'file'}):
        text = file.text
        url = text.split()[0]
        # Select the relevant files
        if ('pages-articles' in url)\
            and ('xml-p' in url)\
                and ('multistream' not in url):
            files.append((url, text.split()[1:]))
    return files
