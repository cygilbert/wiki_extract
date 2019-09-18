"""
Download functions
    Module of functions to download and store the
    latest version of the english wikipedia dump
"""

import requests
import os
import urllib
from bs4 import BeautifulSoup


def get_soup_from_url(url="https://en.wikipedia.org/wiki/English_Wikipedia"):

    '''
    Get BeautifulSoup content of web page from its url

    param url: the url of the web page
    type url: string

    return: BeautifulSoup content of the page
    rtype: bs4.BeatufulSoup
    '''

    index = requests.get(url).text
    return BeautifulSoup(index, 'html.parser')


def get_wikidump_url(base_url="https://dumps.wikimedia.org/enwiki/"):

    '''
    Get the latest wikidump version of english wikipedia from the dump rep url

    param base_url: the url of the english wikipedia dump rep
    type base_url: string

    return: the url of the latest version of english wikipedia dump
    rtype: string
    '''

    soup_index = get_soup_from_url(base_url)
    dumps_list = [
        a['href'] for a in soup_index.find_all('a')
        if a.has_attr('href')
    ]
    return base_url + dumps_list[-2]


def get_list_downloads_wikidump(
        dump_url="https://dumps.wikimedia.org/enwiki/20190901/"
        ):

    '''
    Get the files of interest from the latest wikipedia dump url

    param dump_url: the url of the latest english wikipedia dump
    type base_url: string

    return: list of tuples (url of files, size of files)
    rtype: list
    '''

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


def download_file(
        url='https://dumps.wikimedia.org/enwiki/20190901/' +
            'enwiki-20190901-pages-articles14.xml-p7697599p7744799.bz2'):

    '''
    Get file from its url

    param url: url of the file
    type base_url: string

    return: file downloaded
    rtype: http.client.HTTPResponse
    '''

    filedata = urllib.request.urlopen(url)
    return filedata


def get_file_from_url(
        url='https://dumps.wikimedia.org/enwiki/20190901/' +
            'enwiki-20190901-pages-articles14.xml-p7697599p7744799.bz2',
        target_folder="temp_files/"):

    '''
    Get file from its url and store it in target_folder
    If the folder does not exist, make it
    The function does not download the file if it already exists
    in target_folder

    param url: url of the file
    param target_folder: folder where to write the file
    type base_url: string
    type target_folder: string

    return: file name and target_folder
    rtype1: string
    rtype2: string
    '''

    file_name = url.split('/')[-1]
    file_path = target_folder + file_name
    if not(os.path.isdir(target_folder)) and (target_folder != ""):
        os.mkdir(target_folder)
    if not os.path.exists(file_path):
        print('downloading ' + file_name + '...')
        datatowrite = download_file(url).read()
        with open(file_path, 'wb') as f:
            f.write(datatowrite)
        print(file_name + ' downloaded !')
    else:
        print(file_name + ' already exists !')
    return file_name, target_folder
