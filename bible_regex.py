# -*- coding: cp1252 -*-
"""
match bible refs.
"""
import re
import bible_books

class RegExTerm():
    """
    Superclass for various terms of the Bible regex.
    For each term of the regex, you create an object, optionally pass in a
    list of acceptable values for that term with the .include method, then
    assign the value returned by the .construct method to a variable.
    See code in BibleRefRegEx for examples.
    """
    def __init__(self, optional=False):
        self.main_list = []
        self.optional = optional

    def include(self, a_list):
        """
        This method adds a list of options to the term.
        """
        self.main_list.extend(a_list)

    def construct(self, verbose=False):
        """
        Turn the main list into a regex
        """
        self.main_list = self._make_set(self.main_list)
        self.main_list = self._sort(self.main_list)
        if self._single_chars_only(self.main_list):
            result = u'[%s]' % ''.join(self.main_list)
        else:
            result = u'(%s)' % '|'.join(self.main_list)
        if self.optional:
            result = u'%s?' % result
        result = self._escape_chars(result, verbose)
        return result

    def _make_set(self, a_list):
        """
        Derive list containing unique set of items from list.
        """
        set_list = set(a_list)
        return [item for item in set_list]

    def _sort(self, a_list):
        """
        Sort the list.
        Default is from longest to shortest. This makes the regex
        appropriately greedy.
        Override in subclasses as needed.
        """
        a_list.sort(key=len, reverse=True)
        return a_list


    def _escape_chars(self, an_exp, space=False):
        """
        Escape period. Escape space if verbose.
        """
        escaped = an_exp.replace(u'.', u'\.')
        if space:
            escaped = escaped.replace(u' ', u'\ ')
        return escaped

    def _single_chars_only(self, a_list):
        """
        Test whether each item in a list is only 1 character long.
        If so, we can express the regex as a range of chars in brackets.
        Otherwise, have to put it in parentheses with |.
        """
        for item in a_list:
            if len(item) > 1:
                return False
        return True


class SpaceRegEx(RegExTerm):
    """Constructs the regex term for a space.
    Starts with just a regular space.
    Add nbs or other whitespace with include method."""
    def __init__(self, optional=False):
        RegExTerm.__init__(self, optional)
        self.main_list = [u' ']


class RangeMarkerRegEx(RegExTerm):
    """Constructs the regex term for a range marker
    (i.e., the hyphen in Gen 1:2-3).
    """
    def __init__(self, optional=False):
        RegExTerm.__init__(self, optional)
        self.main_list = [u'-', u'\u2013', u'\u2014', u'\u2011']

    def _sort(self, a_list):
        """
        Override the superclass's sort and sort by byte.
        For some reason, hyphen needs to be before dashes or it won't match.
        """
        a_list.sort()
        return a_list

class ChFromVsRegEx(RegExTerm):
    """Constructs the regex term for a separator dividing chapters
    from verses.
    """
    def __init__(self, optional=False):
        RegExTerm.__init__(self, optional)
        self.main_list = [u':']


class RefFromRefRegEx(RegExTerm):
    """Constructs the regex term for a separator dividing one
    reference from another.
    """
    def __init__(self, optional=False):
        RegExTerm.__init__(self, optional)
        self.main_list = [u', ', u'; ',
                         u' and ',
                         u' [ye] ',
                         u', and ', u'; and ',
                         u', [ye] ', u'; [ye] ',
                         ]


class BibleNumberRefRegEx(RegExTerm):
    """Constructs the regex term for a Bible chapter or verse.
    Max of 179 (there are 176 verses in Ps 119), min of 1.
    """
    def __init__(self, optional=False):
        RegExTerm.__init__(self, optional)
        self.main_list = [
            u'1[0-7][0-9]',
            u'[1-9][0-9]',
            u'[1-9]']

    def construct(self, verbose=False):
        """
        Add optional half-verse marker or ff to end of number.
        """
        result = RegExTerm.construct(self)
        return u'%s[a-z]?f?' % result


class CodaRegEx(RegExTerm):
    """
    Not currently used.
    Constructs the regex term for the optional codas after a
    chapter number.
    """
    def __init__(self, optional=True):
        RegExTerm.__init__(self, optional)
        self.main_list = []


class BookNameRegEx(RegExTerm):
    """Object that constructs the regex term for the Bible book names."""
    def __init__(self, optional=False):
        RegExTerm.__init__(self, optional)

    def include(self, a_list):
        """
        When adding book names, add singular "Psalm" and "Salmo"
        Split up Sirach and Ecclesiasticus
        """
        if 'Psalms' in a_list:
            a_list.append('Psalm')
        if 'Salmos' in a_list:
            a_list.append('Salmo')
        if 'Ps' in a_list:
            a_list.append('Pss')
        if 'Sirach (Ecclesiasticus)' in a_list:
            a_list.append('Sirach')
            a_list.append('Ecclesiasticus')
            a_list.append('Sirach \(Ecclesiasticus\)')
            a_list.remove('Sirach (Ecclesiasticus)')
        RegExTerm.include(self, a_list)


class BibleRefRegEx():
    """Grabs bible refs that begin with a book name.
    """
    def __init__(self, book_name_binder):
        booker = BookNameRegEx()
        book_list = book_name_binder.book_list()
        booker.include(book_list)
        #booker.include(['chapter', 'chap', 'ch',
        #    'chapters', 'chaps', 'chs'])
        self.book_names = booker.construct()
        # print self.book_names.encode('utf-8')
        spacer = SpaceRegEx()
        spacer.include([u'\u00a0'])
        self.space = spacer.construct()
        numberer = BibleNumberRefRegEx()
        self.number = numberer.construct()
        ranger = RangeMarkerRegEx()
        self.range_marker = ranger.construct()
        chfromvser = ChFromVsRegEx()
        self.separator_ch_from_vs = chfromvser.construct()
        reffromrefer = RefFromRefRegEx()
        self.separator_ref_from_ref = reffromrefer.construct()

        self.coda = u'(:%s(%s%s(%s%s)?)?|%s%s)?' % (
            self.number,
            self.range_marker,
            self.number,
            self.separator_ch_from_vs,
            self.number,
            self.range_marker,
            self.number
            )
        
        self.with_book = r'%s%s%s%s' % (
            self.book_names,
            self.space,
            self.number,
            self.coda
            )
        self.book_optional = r'(%s%s)?%s%s' % (
            self.book_names,
            self.space,
            self.number,
            self.coda
            )
        self.more_refs = r'%s%s' % (
            self.separator_ref_from_ref,
            self.book_optional
            )
        self.pattern = r'\b%s(%s)*\b' % (
            self.with_book,
            self.more_refs
            )

    def findall(self, text):
        """
        Return all matches in text
        """
        # print self.pattern.encode('utf-8')
        hits = []
        position = 0
        while True:
            hit = re.search(self.pattern, text[position:], re.IGNORECASE)
            if hit is None:
                break
            hits.append(hit.group(0))
            position += hit.end()
        return hits

    def sub(self, replace_method, text):
        """
        Replace each hit with the value defined in replace_method
        """
        text = re.sub(self.pattern, replace_method, text)
        # position = 0
        # while True:
        #     hit = re.search(self.pattern, text[position:], re.IGNORECASE)
        #     if hit is None:
        #         break
        #     replacement_text = replace_method(hit.group(0))
        #     replacement_text = replacement_text.encode('utf-8')
        #     text = text[:position + hit.start()] + replacement_text + text[position + hit.end():]
        #     position += hit.end() + (len(replacement_text) - len(hit.group(0)))
        return text

    def link_bible_ref(self, bible_ref_match):
        """
        A replace method to use with self.sub().
        It turns the bible ref into a link to the first verse of the ref, using 
        the notation from the bibletext repository xml (gene_1_1).
        """
        import bible_parser
        bible_ref = bible_ref_match.group(0)
        crp = bible_parser.CrossReferenceParser()
        for cref in crp.parse(crp.tokenize(bible_ref)):
            # print '%s has these values:\n  bk: %s\n  c1: %s\n  c2: %s\n  v1: %s\n  v2: %s'.encode('utf-8') % (
                # cref.original, cref.book, cref.chapter_first, cref.chapter_last, cref.verse_first, cref.verse_last)
            if cref.ignore == False:
                try:
                    target = cref.link_target()
                except bible_parser.VerseError:
                    pass
                to_return = '<a href="%s">%s</a>' % (target, cref.original)
                bible_ref = bible_ref.replace(cref.original, to_return, 1)
        return bible_ref

    def link_bref(self, bible_ref_match, book_name_binder=None):
        """
        Use Sean's bible ref parser to create bref link on known bible refs.
        Can't get it to work. Import problems.
        """
        import bible_parser
        # import sys
        # import os
        # user_path = os.path.expanduser(r'~\thpy\webdev')
        # if user_path not in sys.path:
        #     sys.path.append(user_path)
        from bibleweb.lib.refparser import RefParser
        from bibleweb import config
        refparser = RefParser(config.connect_to_db())

        bible_ref = bible_ref_match.group(0)
        crp = bible_parser.CrossReferenceParser(book_name_binder=book_name_binder)
        for cref in crp.parse(crp.tokenize(bible_ref)):
            print '%s has these values:\n  bk: %s\n  c1: %s\n  c2: %s\n  v1: %s\n  v2: %s'.encode('utf-8') % (
                cref.original, cref.book, cref.chapter_first, cref.chapter_last, cref.verse_first, cref.verse_last)
            if cref.ignore == False:
                try:
                    print cref.pretty_cref()
                    ref = refparser.parse(cref.pretty_cref())
                    target = refparser.refstring(ref)
                except bible_parser.VerseError:
                    pass
                to_return = '<a href="?bref=%s">%s</a>' % (target, cref.original)
                bible_ref = bible_ref.replace(cref.original, to_return, 1)
        return bible_ref

class CompleteBibleRefRegEx(BibleRefRegEx):
    """
    Grabs bible crefs with or without a book name.
    """
    def __init__(self, book_name_binder):
        BibleRefRegEx.__init__(self, book_name_binder)
        self.required_coda = u'(:%s(%s%s(%s%s)?)?|%s%s)' % (
            self.number,
            self.range_marker,
            self.number,
            self.separator_ch_from_vs,
            self.number,
            self.range_marker,
            self.number
            )
        self.no_book = r'%s%s' % (
            self.number,
            self.required_coda
            # self.coda
            )
        self.pattern = r'\b(%s(%s)*|%s(%s)*)\b' % (
            self.with_book,
            self.more_refs,
            self.no_book,
            self.more_refs
            )

def find_hits():
    fl = open(r'C:\Sandbox\temp\text.xml', 'r')
    text_old = fl.read()
    fl.close()
    # wanted = text_old[text_old.find('Psalms 1'):text_old.find('Psalms 1')+100]
    # print wanted
    bnb = bible_books.BookNameBinder()
    brre = BibleRefRegEx(bnb)
    # hits = brre.findall(text_old)
    hits = re.findall(brre.pattern, text_old)
    for hit in hits:
        print hit
    # text_new = brre.sub(brre.link_bible_ref, text_old)
    # fl = open(r'C:\Sandbox\temp\text.xml', 'w')
    # fl.write(text_new)
    # fl.close()

def replace_hits():
    fl = open(r'C:\Sandbox\temp\text.xml', 'r')
    text_old = fl.read()
    fl.close()
    bnb = bible_books.BookNameBinder()
    brre = BibleRefRegEx(bnb)
    text_new = re.sub(brre.pattern, brre.link_bible_ref, text_old)
    fl = open(r'C:\Sandbox\temp\text.xml', 'w')
    fl.write(text_new)
    fl.close()

def parse_hits():
    fl = open(r'C:\Sandbox\temp\hits.txt', 'r')
    text = fl.read()
    fl.close()
    # splitters = [' and ', ',', ';', '\\n', ':', '\s+', '-']#, u'\u2013', u'\u2014']
    # splitter_string = r'(%s)' % ')('.join(splitters)
    # print splitter_string
    # chunks = re.split(r'( and )|(,)|(;)|(\n)|(:)|(\s+)|(-)', text)
    chunks = re.split(ur'( and |,|;|\n|:|\s+|-|\u2014|\u2013)', text)
    # now walk through chunks
    # and,;\n -> new passage
    # \s+ -> could imply book/chapter. But could split 1 from Corinthians. :-(
    # \s+ -> could be trailing from ,;
    # basically, \s+ tells you nothing.
    # dashes -> range
    
    # print chunks
    # fl = open(r'C:\Sandbox\temp\hit_chunks.txt', 'w')
    # fl.write('\n'.join(chunks))
    # fl.close()

if __name__ == '__main__':
    systems = [
        # bible_books.IVPAbbrDeuterocanon(nbs=u'\u00a0'),
        # bible_books.IVPAbbrDeuterocanon(),
        bible_books.THPFullName(),
        bible_books.THPFullName(nbs=u'\u00a0'),
        # bible_books.THPFullNameDeuterocanon(),
        # bible_books.THPFullNameDeuterocanon(nbs=u'\u00a0'),
        # bible_books.THPSpanishFullName(),
        # bible_books.THPSpanishFullName(nbs=u'\u00a0'),
        # bible_books.THPSpanishBibleTeamAbbr(),
        # bible_books.THPSpanishBibleTeamAbbr(nbs=u'\u00a0'),
        # bible_books.THPFullNameSongs(),
        # bible_books.THPFullNameSongs(nbs=u'\u00a0'),
        # bible_books.SBLFullNameCanticles(),
        # bible_books.SBLFullNameCanticles(nbs=u'\u00a0'),
        # bible_books.SBLFullNameQoheleth(),
        # bible_books.SBLFullNameQoheleth(nbs=u'\u00a0'),
        # bible_books.THPTMSAbbr(),
        # bible_books.THPTMSAbbr(nbs=u'\u00a0'),
        bible_books.THPBibleTeamAbbr(),
        bible_books.THPBibleTeamAbbr(nbs=u'\u00a0'),
        bible_books.THPBibleTeamAbbrHagg(),
        bible_books.THPBibleTeamAbbrHagg(nbs=u'\u00a0'),
        # bible_books.THPLASBIndexAbbr(),
        # bible_books.THPLASBIndexAbbr(nbs=u'\u00a0'),
        # bible_books.HCSBLASBIndexAbbr(),
        # bible_books.HCSBLASBIndexAbbr(nbs=u'\u00a0'),
        # bible_books.THPBibleTeamAbbrDeuterocanon(),
        # bible_books.THPBibleTeamAbbrDeuterocanon(nbs=u'\u00a0'),
        # bible_books.SBLAbbr(),
        # bible_books.SBLAbbr(nbs=u'\u00a0'),
        # bible_books.SBLAbbrCanticles(),
        # bible_books.SBLAbbrCanticles(nbs=u'\u00a0'),
        # bible_books.SBLAbbrQoheleth(),
        # bible_books.SBLAbbrQoheleth(nbs=u'\u00a0'),
        # bible_books.SBLAbbrDeuterocanon(),
        # bible_books.THPBibleTextAbbr(),
        # bible_books.THPBibleTextDeuterocanonAbbr(),
        # bible_books.THPXMLAbbr(),
    ]
    bnb = bible_books.BookNameBinder(systems)
    # brre = BibleRefRegEx(bnb)
    brre = CompleteBibleRefRegEx(bnb)
    # print brre.book_names.encode('utf-8')
    print brre.pattern.encode('utf-8')
    # find_hits()
    # parse_hits()
    # replace_hits()