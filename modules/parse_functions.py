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
    Find all the book articles from a compressed wikipedia XML dump.
   `limit` is an optional argument to only return a set number of books.
    If save, books are saved to partition directory based on file name
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
    """Process a wikipedia article looking for template"""
    # Create a parsing object
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
