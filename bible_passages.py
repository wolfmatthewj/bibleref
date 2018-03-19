#bible_passages.py

class BiblePassage():
    """
    An object representing a passage from the Bible
    A passage should really be a collection of BibleVerses

    attributes:
    .start_verse = BibleVerse
    .end_verse = BibleVerse
    Or, instead of these attributes, this is just a list containing BibleVerse
    objects. If you want to find out anything about the passage (version, 
    language, book), you drill down into those attributes for a BibleVerse
    in the list.

    usage:
    # get the version
    bp = BiblePassage()
    version = bp[0].version
    # get the end verse number
    last_vn = bp[-1].verse_number

    .cross_reference The cross-reference way of pointing to the passage.
        E.g., the collection of BibleVerses Gen 1:1, Gen 1:2, Gen 1:3 should
        have the .cross_reference value of 'Genesis 1:1-3'
    """
    def __init__(self, original_cref):
        self.original_cref = original_cref
        
class BibleBook(BiblePassage):
    """
    A book of the Bible

    A list of BibleChapters? What about one-chapter books? In the real world,
    they are more like a collection of BibleVerses than a 1-length collection
    of BibleChapters. But for consistency, we understand them as having a single
    chapter.

    attributes:
    .book_number or .canonical_number?
    .book_name? Probably better to use the number as a key to a bible_book.BookNameSystem
    """
    def __init__(self, arg):
        BiblePassage.__init__(self)
        self.arg = arg
                
class BibleChapter(BiblePassage):
    """
    A book of the Bible

    A list of BibleVerses

    attributes:
    .chapter_number (number within book)
    .canonical_number (absolute number from beginning of Bible)
    """
    def __init__(self, arg):
        BiblePassage.__init__(self)
        self.arg = arg
        
class BibleVersion():
    """
    A version/translation of the Bible

    attributes:
    .language
    .edition
    .year
    """
    def __init__(self, arg):
        self.arg = arg

class BibleVerse():
    """
    A single verse of the Bible

    attributes:
    .canonical_number For canonical sorting. Gen 1:1 = 000001 # What about Deuterocanon?
    .verse_number
    .book
    .chapter
    .version
    .text Should the text be carried around? Or should these objects just be 
    pointers to the text as stored elsewhere?
    .xml? Distinct from text? Probably not needed.
    .visible For text-critical issues
    .first_paragraph_style
    """
    def __init__(self, arg):
        self.arg = arg
