#!/usr/bin/env python
# modified from http://www.dreamsyssoft.com/python-scripting-tutorial/create-simple-rest-web-service-with-python.php
import web
from lxml import etree
import bible_books
import bible_parser

base_systems = [
            bible_books.THPFullName(),
            bible_books.THPFullName(nbs=u'\u00a0'),
            bible_books.THPFullNameSongs(),
            bible_books.THPBibleTeamAbbr(),
            bible_books.THPBibleTeamAbbr(nbs=u'\u00a0'),
            bible_books.THPNLTSBAbbr(),#Prov and Hagg
            bible_books.THPNLTSBAbbr(nbs=u'\u00a0'),
            bible_books.THPSpanishFullName(),
            bible_books.THPSpanishFullName(nbs=u'\u00a0'),
            bible_books.THPSpanishBibleTeamAbbr(),
            bible_books.THPSpanishBibleTeamAbbr(nbs=u'\u00a0'),
        ]
bnb = bible_books.BookNameBinder(base_systems)

# what urls are acceptable?
urls = (
    '/passages/(.*)', 'get_passages'
)

app = web.application(urls, globals())

class get_passages:
    def GET(self, passages):
        to_return = []
        crp = bible_parser.CrossReferenceParser(
            # bible_version="NTV",
            # default_book="Obadiah",
            book_name_binder=bnb)
        for cref in crp.parse(crp.tokenize(passages)):
            if cref.ignore == False:
                to_return.append(cref.pretty_cref())
                # to_return.append(str((cref.book_number(cref.book), int(cref.chapter_first),
                #     int(cref.chapter_last), int(cref.verse_first), int(cref.verse_last))))
        return '; '.join(to_return)

if __name__ == "__main__":
    app.run()
    # open http://localhost:8080/books/Gen 1