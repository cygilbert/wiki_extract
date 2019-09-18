"""
Unit tests for the project
"""

import os
import mwparserfromhell
from modules.download_functions import get_wikidump_url,\
    get_list_downloads_wikidump, get_soup_from_url, get_file_from_url
from modules.parse_functions import split_articles, get_infobox_article,\
    process_article_with_infobox


class TestDownloadFunctionsUnit:

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


class TestParseFunctions:

    def test_split_articles(self):
        url = 'https://dumps.wikimedia.org/enwiki/20190901/'\
            'enwiki-20190901-pages-articles26.xml-p42567204p42663461.bz2'
        target_folder = "temp_files/"
        file_name, target_folder = get_file_from_url(
            url=url,
            target_folder=target_folder)
        file_path = target_folder + file_name
        articles = split_articles(file_path, stop_iteration=500)
        articles_keys_checked = [
            article for article in articles
            if set(article.keys()) == set(['text', 'timestamp', 'title'])
            ]
        assert len(articles) == len(articles_keys_checked)

    def test_get_infobox_article(self):
        article_text = "{{BLP sources|date=July 2014}} \n \
            {{Infobox ice hockey player \n \
            | name = Marko Virtanenx}}"
        wiki_text = mwparserfromhell.parse(article_text)
        infobox = get_infobox_article(wiki_text)
        assert infobox == {
            'infobox type': 'Infobox ice hockey player',
            'name': 'Marko Virtanenx'}

    def test_process_article(self):
        url = 'https://dumps.wikimedia.org/enwiki/20190901/'\
            'enwiki-20190901-pages-articles26.xml-p42567204p42663461.bz2'
        target_folder = "temp_files/"
        file_name, target_folder = get_file_from_url(
            url=url,
            target_folder=target_folder)
        file_path = target_folder + file_name
        articles = split_articles(file_path, stop_iteration=1000)
        article_infoboxes = list(filter(None, [
            process_article_with_infobox(article)
            for article in articles]))
        print(list(article['infobox'] for article in article_infoboxes))
        assert True
