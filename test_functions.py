"""
Unit tests for the project
"""

import os
from modules.download_functions import get_wikidump_url,\
    get_list_downloads_wikidump, get_soup_from_url, get_file_from_url


class TestDownloadFunctions:

    def test_get_soup_from_url(self):
        soup = get_soup_from_url()
        assert soup.contents

    def test_get_wikidump_url(self):
        dump_url = get_wikidump_url()
        assert "https://dumps.wikimedia.org/enwiki/"\
            in dump_url

    def test_format_date_wikidump_url(self):
        dump_url = get_wikidump_url()
        latest_date = dump_url.split('/')[-2]
        assert (len(latest_date) == 8 and latest_date.isdigit())

    def test_get_list_downloads_wikidump(self):
        dump_url = get_wikidump_url()
        list_url_wikidump = get_list_downloads_wikidump(
            dump_url=dump_url
        )
        assert list_url_wikidump

    def test_list_url_format(self):
        dump_url = get_wikidump_url()
        list_url_wikidump = get_list_downloads_wikidump(
            dump_url=dump_url
            )

        def check_format(url_info):
            url = url_info[0]
            return (
                ('pages-articles' in url)
                and ('xml-p' in url)
                and ('multistream' not in url)
            )
        assert [
            url for url in list_url_wikidump if check_format(url)
        ]

    def test_unicity_list_url(self):
        dump_url = get_wikidump_url()
        list_url_wikidump = get_list_downloads_wikidump(
            dump_url=dump_url
            )
        urls = [url_info[0] for url_info in list_url_wikidump]
        assert len(urls) == len(list(set(urls)))

    def test_get_download_file(self):
        target_folder = "temp_files/"
        # remove previous file
        if not(os.path.isdir(target_folder)) and (target_folder != ""):
            os.mkdir(target_folder)
        else:
            for f in os.listdir(target_folder):
                os.remove(os.path.join(target_folder, f))
        file_name, target_folder = get_file_from_url(
            target_folder=target_folder)
        assert os.path.exists(target_folder + file_name)
