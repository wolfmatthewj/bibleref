#bible_parser.py
"""
parse cross-references
Hope to improve the ref parser from NLT Lookup.
TODO: one-chapter books
TODO: half-verses and ffs--they should be tokenized, but need to add handling 
for them when it comes time to pull data from the db. ff = max, f = start verse + 1
Also need to test half verses.
Half verses should be tokenized properly, but they're not added to pretty_cref.
Should they be?
"""
import re
# import bible_passages
import bible_books
import bible_regex
# import sqlite3
# import complib.xslt
import StringIO

db_path = r'C:\bibletext\_bible.db'

class CrossReferenceParser():
    """
    Given a list of cross-references, return an object for each reference that
    points to the correct database record.
    """
    def __init__(self, bible_version=None, default_book=None,
            book_name_binder=None):
        # set some defaults
        if bible_version == None:
            bible_version = 'nlt'
        if default_book == None:
            default_book = 'Genesis'
        if book_name_binder == None:
            book_name_binder = bible_books.BookNameBinder()

        self.bible_version = bible_version
        self.default_book = default_book
        self.book_name_binder = book_name_binder

        spanish_versions = ['ntv', 'rvr', 'rv60']
        if self.bible_version.lower() in spanish_versions:
            self.is_spanish = True
        else:
            self.is_spanish = False
        # booker = bible_books.BookNameRegEx()
        # booker.include(self.book_name_binder.book_list())
        # book_names = booker.construct()

        # I think I need more patterns--separators, just a chapter
        # need to ignore separators
        # Problem crefs: Hebrews 5:5; and 2 Peter 1:17
        if self.is_spanish:
            self.and_pattern = re.compile(
                ur'([;,])?( y )')
            self.book_pattern = re.compile(
                ur'( y |[;,] ?)?([1-3]( |<nbs/>|\u00a0)?)?([A-Za-z\u00c1\u00c9\u00cd\u00d3\u00da\u00e1\u00e9\u00ed\u00f3\u00fa]{2,})( )(de los Cantares )?')
            self.ch_or_vs_pattern = re.compile(
                ur'( y |[-\u2013\u2014]|[;,] ?)?(\d{1,3})(:)?')
            self.half_verse_pattern = re.compile(
                ur'[A-Za-z]')
            # self.f_pattern = re.compile(
            #     ur'[Ff]')
            self.f_pattern = re.compile(
                ur' ?[Ss]{1,2}')
        else:
            self.and_pattern = re.compile(
                ur'([;,])?( and )')
            self.book_pattern = re.compile(
                ur'( and |[;,] ?)?([1-3]( |<nbs/>|\u00a0)?)?([A-Za-z]{2,})\.?( )(of (Songs|Solomon) )?')
            self.ch_or_vs_pattern = re.compile(
                ur'( and |[-\u2013\u2014]|[;,] ?)?(\d{1,3})(:)?')
            self.half_verse_pattern = re.compile(
                ur'[A-Za-z]')
            # self.f_pattern = re.compile(
            #     ur'[Ff]')
            self.f_pattern = re.compile(
                ur'[Ff]{1,2}')

    def tokenize(self, reference_string):
        """
        Imitating dalkescientific.com/writings/NBN/parsing_by_hand.html
        """
        N = len(reference_string)
        pos = 0
        active_colon = False
        while pos < N:
            m = self.and_pattern.match(reference_string, pos)
            if m:
                yield ("and", pos, m.group())
                # if DEBUG:
                # print 'yielded %s as "and"' % m.group().encode('utf-8')
                pos = m.end()
                continue
            m = self.book_pattern.match(reference_string, pos)
            # print reference_string.encode('utf-8')
            if m:
                yield ("book", pos, m.group())
                # if 'Cantar' in reference_string:
                # print 'yielded %s as "book"' % m.group().encode('utf-8')
                pos = m.end()
                active_colon = False
                continue
            m = self.ch_or_vs_pattern.match(reference_string, pos)
            if m:
                if active_colon and ':' not in m.group():
                    yield ("verse", pos, m.group())
                    # if DEBUG:
                    # print 'yielded %s as "verse"' % m.group().encode('utf-8')
                    pos = m.end()
                    continue
                else:
                    yield ("chapter", pos, m.group())
                    # if DEBUG:
                    # print 'yielded %s as "chapter"' % m.group().encode('utf-8')
                    pos = m.end()
                    if ':' in m.group():
                        active_colon = True
                    continue
            m = self.f_pattern.match(reference_string, pos)
            if m:
                yield ("verse", pos, m.group())
                # if DEBUG:
                # print 'yielded %s as "verse"' % m.group().encode('utf-8')
                pos = m.end()
                continue
            m = self.half_verse_pattern.match(reference_string, pos)
            if m:
                yield ("half-verse", pos, m.group())
                # if DEBUG:
                # print 'yielded %s as "half-verse"' % m.group().encode('utf-8')
                pos = m.end()
                continue
            m = self.f_pattern.match(reference_string, pos)
            if m:
                yield ("half-verse", pos, m.group())
                # if DEBUG:
                # print 'yielded %s as "half-verse"' % m.group().encode('utf-8')
                pos = m.end()
                continue
            raise TypeError('Unknown text at position %d (%r)' %
                (pos, reference_string))

    def new_passage(self, token_type, token):
        """
        Determine whether a token is the beginning of a new passage
        """
        if token_type == 'book':# or token_type == 'and':
            return True
        separators = [',', ';', ' and ', ' y ', ' e ']
        for sep in separators:
            if sep in token:
                return True
        return False

    def parse(self, tokens):
        """
        Take a list or iterator returning tokens; yield BibleCrossReference
        Glue each token on to a BibleCrossReference until a new one starts.
        """
        token_stream = iter(tokens)
        cref = None
        book = None
        chapter = None

        for token_type, pos, token in token_stream:
            if self.new_passage(token_type, token):
                if cref is not None:
                    yield cref
                cref = BibleCrossReference(self.bible_version,
                    self.book_name_binder)
            if token_type == 'and':
                cref.glue(token_type, token)
            if token_type == 'book':
                if token == None:
                    cref.glue('book', book, carryover=True)
                else:
                    cref.glue(token_type, token)
                    book = token
            if token_type == 'chapter':
                if cref is None:
                    cref = BibleCrossReference(self.bible_version,
                        self.book_name_binder)
                    book = self.default_book
                cref.glue('book', book, carryover=True)
                cref.glue(token_type, token)
                chapter = token
            if token_type == 'verse':
                cref.glue('book', book, carryover=True)
                cref.glue('chapter', chapter, carryover=True)
                cref.glue(token_type, token)
            if token_type == 'half-verse':
                cref.glue(token_type, token)
        yield cref


class BibleCrossReference():
    """
    An object that stores the crucial data about a cross-reference
    """
    def __init__(self, bible_version, book_name_binder):
        self.bible_version = bible_version
        self.book_name_binder = book_name_binder# a bible_books.BookNameBinder object
        self.book = None
        self.chapter_first = None
        self.chapter_last = None
        self.verse_first = None
        self.verse_last = None
        self.original = ''
        self.ignore = False

    def glue(self, token_type, token, carryover=False):
        """
        Assimilate the token information
        """
        if token_type == 'and':
            self.ignore = True
        else:
            self.ignore = False
        if token_type == 'book':
            # print 'token is "%s"' % token
            self.book = self.book_clean(token)
            # print 'resulting book is "%s"' % self.book
        elif token_type == 'chapter':
            if self.chapter_first:
                self.chapter_last = self.clean(token)
            else:
                self.chapter_first = self.clean(token)
                self.chapter_last = self.clean(token)
        elif token_type == 'verse':
            if self.verse_first:
                self.verse_last = self.clean(token)
            else:
                self.verse_first = self.clean(token)
                self.verse_last = self.clean(token)
        if not carryover:
            self.original += token

    def pretty_cref(self):
        # print self.book, len(self.book)
        pretty = '%s ' % self.book_name(self.book_number(self.book))
        pretty += self.chapter_first
        if self.chapter_last != self.chapter_first:
            pretty_chap = u'\u2013%s' % self.chapter_last
            if self.verse_last != self.verse_first:
                pretty_chap += ':%s' % self.verse_last
        else:
            pretty_chap = ''
            if self.verse_last != self.verse_first:
                pretty_chap += '-%s' % self.verse_last
        if self.verse_first:
            pretty += ':%s' % self.verse_first
        pretty += pretty_chap
        return pretty

    def clean(self, token):
        """
        Remove extraneous matter from the token
        Keep only the number
        """
        token = re.sub(r'[^\d]', '', token)
        return token

    def book_clean(self, token):
        """
        use a regex and match the acceptable book names/abbr.
        """
        b_list = self.book_name_binder.book_list()
        # escape periods
        b_list = [b.replace(u'.', u'\.') for b in b_list]
        b_list.sort(key=len, reverse=True)
        # print '|'.join(b_list)
        pat = re.compile('|'.join(b_list), re.IGNORECASE)
        m = re.search(pat, token)
        # print m.group()
        if m is not None:
            return m.group()
        return None

    def book_number(self, book_name):
        # needs to continue if the book name isn't in there for some reason
        bn_dict = self.book_name_binder.book_name_to_number()
        try:
            bn = bn_dict[book_name]
        except KeyError:
            raise VerseError(self.original)
        # print book_name
        return bn

    def book_name(self, book_number):
        """
        Use the first book_name_system in the binder for the pretty name
        """
        bns = self.book_name_binder.book_name_systems[0]
        return bns.book_dict[book_number]

    def sql_string(self, book, chapter, verse):
        """
        Convert object attributes into sql query
        """
        if verse == 'max':
            query = (
                'SELECT * FROM %s '
                'WHERE book_num = %d '
                'AND chapter_num = %s '
                'ORDER BY verse_num DESC' % (
                    self.bible_version,
                    self.book_number(book),
                    chapter,
                    )
                )
        else:
            query = (
                'SELECT * FROM %s '
                'WHERE book_num = %d '
                'AND chapter_num = %s '
                'AND verse_num = %s' % (
                    self.bible_version,
                    self.book_number(book),
                    chapter,
                    verse,
                    )
                )
        return query

    def get_start_verse(self, the_cursor):
        verse = the_cursor.execute(self.sql_string(self.book,
            self.chapter_first,
            self.verse_first or '1'))
        start = the_cursor.fetchone()
        # non-existent verses
        if start == None:
            raise VerseError(self.original)
        # redirects
        while start['see'] == 'previous':
            verse = the_cursor.execute(
                'SELECT * FROM %s '
                'WHERE Id = %d' % (
                    self.bible_version,
                    start['Id'] - 1)
                )
            start = the_cursor.fetchone()
        return start

    def get_end_verse(self, the_cursor):
        verse = the_cursor.execute(self.sql_string(self.book,
            self.chapter_last,
            self.verse_last or 'max'))
        end = the_cursor.fetchone()
        # non-existent verses
        if end == None:
            raise VerseError(self.original)
        # redirects
        while end['see'] == 'next':
            verse = the_cursor.execute(
                'SELECT * FROM %s '
                'WHERE Id = %d' % (
                    self.bible_version,
                    end['Id'] + 1)
                )
            end = the_cursor.fetchone()
        return end

    def link_target(self):
        """
        Return the href that points to the first verse in the cref
        """
        book_num = self.book_number(self.book)
        bns = bible_books.THPBibleTextAbbr()
        book = bns.book_dict[book_num]
        chap = self.chapter_first
        verse = self.verse_first or '1'
        # print '%s has the following vals: book: %s, chapter: %s, verse: %s' % (self.original, book, chap, verse)
        return '%s_%s_%s' % (book, chap, verse)

    def get_passage(self):
        """
        Take the cross-reference details and return the passage.
        This is where we need to access the relevant table of the db.
        """
        import sqlite3
        # by importing here instead of at the top of the module, we can use
        # this module in Sublime Text plugins
        connect = sqlite3.connect(db_path)
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        start = self.get_start_verse(cursor)
        end = self.get_end_verse(cursor)
        if int(start['Id']) > int(end['Id']):
            raise VerseError(self.original)
        verses = cursor.execute(
            'SELECT * from %s '
            'WHERE Id BETWEEN %d AND %d '
            'ORDER BY Id' % (
                self.bible_version,
                start['Id'],
                end['Id'])
            )
        passage = cursor.fetchall()
        # print '%d verses in passage %s' % (len(passage), self.original)
        connect.close()
        return passage

    def add_starts_ends(self, xml_text, class_context):
        """
        Index -starts and -ends
        if first -start > first -end: add -start
        if last -end < last -start: add -end
        Handle -1
        """
        # print xml_text, class_context
        element, cls = class_context.split('.')
        first_start = xml_text.find('<%s-start' % element)
        first_end = xml_text.find('<%s-end' % element)
        last_start = xml_text.rfind('<%s-start' % element)
        last_end = xml_text.rfind('<%s-end' % element)
        # print first_start, first_end, last_start, last_end
        if first_start == -1 or (first_start > first_end and first_end != -1):
            xml_text = '<%s-start class="%s"/>\n%s' % (element, cls, xml_text)
        if first_end == -1 or last_end < last_start:
            xml_text = '%s<%s-end/>' % (xml_text, element)
        return xml_text

    def orient_to_paragraph(self, passage_xml,
            included_stylesheets):
        """
        Transform from verse-oriented to paragraph-oriented xml.
        """
        import complib.xslt
        stylesheet = open(r'xsl/copy_all.xsl', 'r').read()
        includes = '\n'.join(
            ['<xsl:include href="%s"/>' % ss for ss in included_stylesheets])
        stylesheet = stylesheet.replace('<xsl:template ',
            '%s\n<xsl:template ' % includes,
            1)
        fl = open(r'xsl/main.xsl', 'w')
        fl.write(stylesheet)
        fl.close()
        result = StringIO.StringIO()
        passage_xml = '<passage-reference>%s</passage-reference>\n%s' % (
            self.pretty_cref(), passage_xml)
        passage_xml = '<passage>\n%s</passage>' % passage_xml
        stylesheet = complib.xslt.XSLT(r'xsl/main.xsl')
        # stylesheet = complib.xslt.XSLT('paragraph.xsl')
        passage_xml = stylesheet.transform(passage_xml)
        passage_xml.write(result, method='xml', encoding='utf-8')
        passage_xml = result.getvalue()
        return passage_xml

    def xml(self, included_stylesheets=['paragraph.xsl']):
        """
        Resolve the passage into valid xml
        """
        passage = self.get_passage()
        passage_xml = '\n'.join([verse['verse_text'] for verse in passage])
        passage_xml = self.add_starts_ends(passage_xml,
            passage[0]['class_context'])
        passage_xml = self.orient_to_paragraph(passage_xml,
            included_stylesheets)
        return passage_xml


class VerseError(Exception):
    """
    """
    def __init__(self, original):
        self.original = original

    def __str__(self):
        return 'Could not resolve cross-reference: %s' % self.original
        
        
def tester():
    systems = [
        bible_books.THPFullName(),
        bible_books.THPFullName(nbs=u'\u00a0'),
        bible_books.THPFullName(nbs=u'<nbs/>'),
        bible_books.THPBibleTeamAbbr(),
        bible_books.THPBibleTeamAbbr(nbs=u'\u00a0'),
        bible_books.THPBibleTeamAbbr(nbs=u'<nbs/>'),
        ]
    bnb = bible_books.BookNameBinder(systems)
    fl = open(r'C:\Sandbox\temp\hits.txt', 'r')
    text = fl.read()
    fl.close()
    crp = CrossReferenceParser('nlt_uk', 'Genesis', bnb)
    fl = open(r'C:\Sandbox\temp\hit_chunks_parsed.txt', 'w')
    for line in text.split('\n'):
        for passage in crp.parse(crp.tokenize(line)):
            fl.write('orig=%s\n' % passage.original)
            fl.write('book=%s\n' % passage.book)
            fl.write('c1=%s\n' % passage.chapter_first)
            fl.write('c2=%s\n' % passage.chapter_last)
            fl.write('v1=%s\n' % passage.verse_first)
            fl.write('v2=%s\n\n' % passage.verse_last)
    fl.close()

def small_test():
    # bnb = bible_books.BookNameBinder()
    # crp = CrossReferenceParser('nlt_uk', 'Genesis', bnb)
    bnb = bible_books.BookNameBinder([bible_books.THPFullName(),
        bible_books.SwindollStudyBibleAbbr(),
            bible_books.SwindollStudyBibleAbbr(nbs=u'\u00a0'),])
    print 'Psalm' in bnb.book_list()
    crp = CrossReferenceParser(
        default_book='Genesis',
        book_name_binder=bnb)
    for cref in crp.parse(crp.tokenize(u'Psalm 34')):
        print cref.pretty_cref()
        # print cref.xml()

def retrieve_test():
    fl = open(r'C:\Sandbox\temp\hits.txt', 'r')
    text = fl.read()
    fl.close()
    systems = [
        bible_books.THPFullName(),
        bible_books.THPFullName(nbs=u'\u00a0'),
        bible_books.THPFullName(nbs=u'<nbs/>'),
        bible_books.THPBibleTeamAbbr(),
        bible_books.THPBibleTeamAbbr(nbs=u'\u00a0'),
        bible_books.THPBibleTeamAbbr(nbs=u'<nbs/>'),
        ]
    bnb = bible_books.BookNameBinder(systems)
    crp = CrossReferenceParser('nlt_uk', 'Genesis', bnb)
    fl = codecs.open(r'C:\Sandbox\temp\hit_passages.txt', 'w', encoding='utf-8')
    for line in text.split('\n'):
        try:
            for cref in crp.parse(crp.tokenize(line)):
                # fl.write(cref.pretty_cref())
                # fl.write('\n')
                try:
                    fl.write(cref.xml())
                except UnicodeDecodeError:
                    fl.write(cref.xml().decode('utf-8', 'replace'))
                fl.write('\n\n')
        except VerseError as X:
            fl.write(str(X))
            fl.write('\n\n')
    fl.close()

if __name__ == '__main__':
    import codecs
    # tester()
    small_test()
    # retrieve_test()