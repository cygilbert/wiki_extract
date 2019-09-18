import xml.sax
import bz2


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
    # Iterate through compressed file
    # for i, line in enumerate(subprocess.Popen(['bzcat'],
    #                          stdin = open(data_path),
    #                          stdout = subprocess.PIPE).stdout):
    for i, line in enumerate(bz2.BZ2File(data_path, 'r')):
        parser.feed(line)
        if stop_iteration and (i > stop_iteration):
            break
    return handler._pages
