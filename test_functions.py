"""
Unit tests for the project
"""

from modules.download_functions import get_wikidump_url


class TestDownloadFunctions:

    def test_get_wikidump_url(self):
        dump_url = get_wikidump_url()
        assert (dump_url is not None)
