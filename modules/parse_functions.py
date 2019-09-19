"""
Parse functions
    Module of functions to parse wikipedia dump
    downloaded with download_functions module
"""

import xml.sax
import bz2
import mwparserfromhell


class WikiXmlHandlerSplit(xml.sax.handler.ContentHandler):
    """Parse through XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._books = []
        self._article_count = 0
        self._non_matches = []
        self._pages = []

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text', 'timestamp'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            self._article_count += 1
            # Append to the list of articles
            page = self._values.copy()
            self._pages.append(page)


def split_articles(data_path, stop_iteration=False):

    """
    Split a wikidump file into wikipedia articles

    param datapath: the path of the wikipedia dump file
    param stop_itearation: number of line max to
    read in the wikidump file. If False, read all the file
    type data: string
    type stop_iteration: int

    return: list of wikipedia articles
    rtype: list of dictionnary
    """

    # Object for handling xml
    handler = WikiXmlHandlerSplit()
    # Parsing object
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    for i, line in enumerate(bz2.BZ2File(data_path, 'r')):
        parser.feed(line)
        if stop_iteration and (i > stop_iteration):
            break
    return handler._pages


def get_infobox_article(wiki_text):

    """
    Get the infobox from the text of an article if it exists
    please visit : https://en.wikipedia.org/wiki/Help:Infobox
    for more informations

    param wiki_text: the text of an article
    type wiki_text: string

    return: wikipedia infobox if it existes, False otherwise
    rtype: dictionary
    """

    try:
        infobox = [
            template for template in wiki_text.filter_templates()
            if "Infobox" in template.name][0]
        information = {
            param.name.strip_code().strip(): param.value.strip_code().strip()
            for param in infobox.params
        }
        information['infobox type'] = infobox.name.strip_code().strip()
        return information
    except IndexError:
        return False


def process_article_with_infobox(article):

    """
    Enrich an article with infobox info, wikilinks,
    external links and text length

    param article: an article with ['text', 'timestamp',
    'title'] as keys list
    type wiki_text: dictionary

    return: an article with ['text', 'timestamp',
    'title', infobox, exlinks, wikilinks, text_length]
    as keys list
    rtype: dictionary
    """

    wiki_text = mwparserfromhell.parse(article['text'])
    # Search through templates for the template
    article['infobox'] = get_infobox_article(wiki_text)
    if article['infobox']:
        # Extract internal wikilinks
        article['wikilinks'] = [
            x.title.strip_code().strip()
            for x in wiki_text.filter_wikilinks()
        ]
        # Extract external links
        article['exlinks'] = [
            x.url.strip_code().strip()
            for x in wiki_text.filter_external_links()
        ]
        # Find approximate length of article
        article['text_length'] = len(wiki_text.strip_code().strip())
        return article
