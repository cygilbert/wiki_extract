"""
Unit tests for the project
"""

from modules.download_functions import get_wikidump_url, get_list_url_wikidump


class TestDownloadFunctions:

    def test_get_wikidump_url(self):
        dump_url = get_wikidump_url()
        assert (dump_url is not None)

    def test_get_list_url_wikidump(self):
        dump_url = get_wikidump_url()
        list_url_wikidump = get_list_url_wikidump(
            dump_url=dump_url
        )
        assert list_url_wikidump
