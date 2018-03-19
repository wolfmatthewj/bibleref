"""
Objects for Bible book naming systems
TODO: Need a strategy for adding Deuterocanon and getting the right sort.
39.1, 39.2, 39.3, etc?
"""
import codecs

class BookNameSystem():
    """
    Superclass for systems
    Starts with an empty dictionary. Each subclass has a dictionary of changes
    to the main dictionary. This allows subclasses to inherit parts of the
    dictionary.
    """
    def __init__(self, nbs):
        """
        The nbs parameter allows the user to pass in the string that should
        be used to separate book numbers from book names.
        Default is a regular space, even though the dictionaries contain
        nonbreaking spaces. It's easier to remove them by default than to 
        try to add them in when they're needed.
        """
        self.book_dict = {}
        self.nbs = nbs

    def _alter_dict(self):
        """
        Update the main dictionary with the changes
        """
        self.book_dict.update(self.changes)
        if self.nbs != u'\u00a0':
            self._replace_nbs()

    def _replace_nbs(self):
        """
        Replace nonbreaking spaces with their proper representation.
        """
        for key in self.book_dict.keys():
            self.book_dict[key] = self.book_dict[key].replace(u'\u00a0',
                self.nbs)

    def book_list(self):
        """
        Return a list of the books in order
        """
        keys = sorted(self.book_dict.keys())
        return [self.book_dict[key] for key in keys]


class THPFullName(BookNameSystem):
    """The full name of books in THP's standard"""
    def __init__(self, nbs=u' '):
        BookNameSystem.__init__(self, nbs=nbs)
        self.lang = 'en'
        self.changes = {
            1: u'Genesis',
            2: u'Exodus',
            3: u'Leviticus',
            4: u'Numbers',
            5: u'Deuteronomy',
            6: u'Joshua',
            7: u'Judges',
            8: u'Ruth',
            9: u'1\u00a0Samuel',
            10: u'2\u00a0Samuel',
            11: u'1\u00a0Kings',
            12: u'2\u00a0Kings',
            13: u'1\u00a0Chronicles',
            14: u'2\u00a0Chronicles',
            15: u'Ezra',
            16: u'Nehemiah',
            17: u'Esther',
            18: u'Job',
            19: u'Psalms',
            20: u'Proverbs',
            21: u'Ecclesiastes',
            22: u'Song of Solomon',
            23: u'Isaiah',
            24: u'Jeremiah',
            25: u'Lamentations',
            26: u'Ezekiel',
            27: u'Daniel',
            28: u'Hosea',
            29: u'Joel',
            30: u'Amos',
            31: u'Obadiah',
            32: u'Jonah',
            33: u'Micah',
            34: u'Nahum',
            35: u'Habakkuk',
            36: u'Zephaniah',
            37: u'Haggai',
            38: u'Zechariah',
            39: u'Malachi',
            40: u'Matthew',
            41: u'Mark',
            42: u'Luke',
            43: u'John',
            44: u'Acts',
            45: u'Romans',
            46: u'1\u00a0Corinthians',
            47: u'2\u00a0Corinthians',
            48: u'Galatians',
            49: u'Ephesians',
            50: u'Philippians',
            51: u'Colossians',
            52: u'1\u00a0Thessalonians',
            53: u'2\u00a0Thessalonians',
            54: u'1\u00a0Timothy',
            55: u'2\u00a0Timothy',
            56: u'Titus',
            57: u'Philemon',
            58: u'Hebrews',
            59: u'James',
            60: u'1\u00a0Peter',
            61: u'2\u00a0Peter',
            62: u'1\u00a0John',
            63: u'2\u00a0John',
            64: u'3\u00a0John',
            65: u'Jude',
            66: u'Revelation'
        }
        self._alter_dict()

class THPFullNameDeuterocanon(THPFullName):
    """The full names of the Deuterocanon"""
    def __init__(self, nbs=u' '):
        THPFullName.__init__(self, nbs=u' ')
        self.changes = {
            16.1: u'Tobit',
            16.2: u'Judith',
            17.1: u'1\u00a0Maccabees',
            17.2: u'2\u00a0Maccabees',
            22.1: u'Wisdom',
            # 22.1: u'Wisdom of Solomon',
            22.2: u'Sirach (Ecclesiasticus)',
            25.1: u'Baruch',
        }
        self._alter_dict()

class THPSpanishFullName(BookNameSystem):
    """The full name of books in THP's Spanish standard"""
    def __init__(self, nbs=u' '):
        BookNameSystem.__init__(self, nbs=nbs)
        self.lang = 'en'
        self.changes = {
            1: u'G\u00E9nesis',
            2: u'\u00c9xodo',
            3: u'Lev\u00EDtico',
            4: u'N\u00FAmeros',
            5: u'Deuteronomio',
            6: u'Josu\u00E9',
            7: u'Jueces',
            8: u'Rut',
            9: u'1\u00a0Samuel',
            10: u'2\u00a0Samuel',
            11: u'1\u00a0Reyes',
            12: u'2\u00a0Reyes',
            13: u'1\u00a0Cr\u00F3nicas',
            14: u'2\u00a0Cr\u00F3nicas',
            15: u'Esdras',
            16: u'Nehem\u00EDas',
            17: u'Ester',
            18: u'Job',
            19: u'Salmos',
            20: u'Proverbios',
            21: u'Eclesiast\u00E9s',
            22: u'Cantar\u00a0de los Cantares',
            23: u'Isa\u00EDas',
            24: u'Jerem\u00EDas',
            25: u'Lamentaciones',
            26: u'Ezequiel',
            27: u'Daniel',
            28: u'Oseas',
            29: u'Joel',
            30: u'Am\u00F3s',
            31: u'Abd\u00EDas',
            32: u'Jon\u00E1s',
            33: u'Miqueas',
            34: u'Nah\u00FAm',
            35: u'Habacuc',
            36: u'Sofon\u00EDas',
            37: u'Hageo',
            38: u'Zacar\u00EDas',
            39: u'Malaqu\u00EDas',
            40: u'Mateo',
            41: u'Marcos',
            42: u'Lucas',
            43: u'Juan',
            44: u'Hechos',
            45: u'Romanos',
            46: u'1\u00a0Corintios',
            47: u'2\u00a0Corintios',
            48: u'G\u00E1latas',
            49: u'Efesios',
            50: u'Filipenses',
            51: u'Colosenses',
            52: u'1\u00a0Tesalonicenses',
            53: u'2\u00a0Tesalonicenses',
            54: u'1\u00a0Timoteo',
            55: u'2\u00a0Timoteo',
            56: u'Tito',
            57: u'Filem\u00F3n',
            58: u'Hebreos',
            59: u'Santiago',
            60: u'1\u00a0Pedro',
            61: u'2\u00a0Pedro',
            62: u'1\u00a0Juan',
            63: u'2\u00a0Juan',
            64: u'3\u00a0Juan',
            65: u'Judas',
            66: u'Apocalipsis',
}
        self._alter_dict()


class THPFullNameSongs(THPFullName):
    """Song of Songs instead of Song of Solomon"""
    def __init__(self, nbs=u' '):
        THPFullName.__init__(self, nbs=nbs)
        self.changes = {
            22: u'Song of Songs',
        }
        self._alter_dict()

class SBLFullNameCanticles(THPFullName):
    """Canticles instead of Song of Songs"""
    def __init__(self, nbs=u' '):
        THPFullName.__init__(self, nbs=nbs)
        self.changes = {
            22: u'Canticles',
        }
        self._alter_dict()


class SBLFullNameQoheleth(THPFullName):
    """Qoheleth instead of Ecclesiastes"""
    def __init__(self, nbs=u' '):
        THPFullName.__init__(self, nbs=nbs)
        self.changes = {
            21: u'Qoheleth',
        }
        self._alter_dict()


class THPTMSAbbr(THPFullName):
    """abbreviations from Tyndale Manual of Style"""
    def __init__(self, nbs=u' ', period=True):
        THPFullName.__init__(self, nbs=nbs)
        self.changes = {
            1: u'Gen.',
            2: u'Exod.',
            3: u'Lev.',
            4: u'Num.',
            5: u'Deut.',
            6: u'Josh.',
            7: u'Judg.',
            9: u'1\u00a0Sam.',
            10: u'2\u00a0Sam.',
            13: u'1\u00a0Chron.',
            14: u'2\u00a0Chron.',
            16: u'Neh.',
            19: u'Ps.',
            20: u'Prov.',
            21: u'Eccles.',
            22: u'Song',
            23: u'Isa.',
            24: u'Jer.',
            25: u'Lam.',
            26: u'Ezek.',
            27: u'Dan.',
            28: u'Hos.',
            31: u'Obad.',
            32: u'Jon.',
            33: u'Mic.',
            34: u'Nah.',
            35: u'Hab.',
            36: u'Zeph.',
            37: u'Hag.',
            38: u'Zech.',
            39: u'Mal.',
            40: u'Matt.',
            45: u'Rom.',
            46: u'1\u00a0Cor.',
            47: u'2\u00a0Cor.',
            48: u'Gal.',
            49: u'Eph.',
            50: u'Phil.',
            51: u'Col.',
            52: u'1\u00a0Thes.',
            53: u'2\u00a0Thes.',
            54: u'1\u00a0Tim.',
            55: u'2\u00a0Tim.',
            57: u'Philem.',
            58: u'Heb.',
            60: u'1\u00a0Pet.',
            61: u'2\u00a0Pet.',
            66: u'Rev.'
        }
        self._alter_dict()
        if period == False:
            self._remove_period()

    def _remove_period(self):
        for key in self.book_dict.keys():
            self.book_dict[key] = self.book_dict[key].replace(u'.', u'')


class THPBibleTeamAbbr(THPTMSAbbr):
    """
    abbreviations used by THP Bible team
    """
    def __init__(self, nbs=u' ', period=False):
        THPTMSAbbr.__init__(self, nbs=nbs, period=False)
        self.changes = {
            11: u'1\u00a0Kgs',
            12: u'2\u00a0Kgs',
            13: u'1\u00a0Chr',
            14: u'2\u00a0Chr',
            17: u'Esth',
            20: u'Pr',
            21: u'Eccl',
            57: u'Phlm',
            59: u'Jas',
            62: u'1\u00a0Jn',
            63: u'2\u00a0Jn',
            64: u'3\u00a0Jn',
        }
        self._alter_dict()

class SwindollStudyBibleAbbr(THPTMSAbbr):
    """
    abbreviations used in the Swindoll Study Bible
    """
    def __init__(self, nbs=u' ', period=True):
        THPTMSAbbr.__init__(self, nbs=nbs, period=True)
        self.changes = {
            11: u'1\u00a0Kgs.',
            12: u'2\u00a0Kgs.',
            13: u'1\u00a0Chr.',
            14: u'2\u00a0Chr.',
            17: u'Esth.',
            20: u'Prov.',
            21: u'Eccl.',
            57: u'Phlm.',
            59: u'Jas.',
            62: u'1\u00a0Jn.',
            63: u'2\u00a0Jn.',
            64: u'3\u00a0Jn.',
        }
        self._alter_dict()

class THPBibleTeamAbbrHagg(THPBibleTeamAbbr):
    """
    Sean's bible process requires Hagg instead of Hag
    """
    def __init__(self, nbs=u' ', period=False):
        THPBibleTeamAbbr.__init__(self, nbs=nbs, period=False)
        self.changes = {
            37: u'Hagg',
        }
        self._alter_dict()

class THPNLTSBAbbr(THPBibleTeamAbbrHagg):
    """
    NLTSB has Hagg and Prov
    """
    def __init__(self, nbs=u' ', period=False):
        THPBibleTeamAbbrHagg.__init__(self, nbs=nbs, period=False)
        self.changes = {
            20: u'Prov',
        }
        self._alter_dict()

class THPSpanishBibleTeamAbbr(THPTMSAbbr):
    """
    abbreviations used by THP Spanish Bible team
    """
    def __init__(self, nbs=u' ', period=False):
        THPTMSAbbr.__init__(self, nbs=nbs, period=False)
        self.changes = {
            1: u'Gn',
            2: u'Ex',
            3: u'Lv',
            4: u'Nm',
            5: u'Dt',
            6: u'Jos',
            7: u'Jc',
            8: u'Rt',
            9: u'1\u00a0Sm',
            10: u'2\u00a0Sm',
            11: u'1\u00a0Re',
            12: u'2\u00a0Re',
            13: u'1\u00a0Cr',
            14: u'2\u00a0Cr',
            15: u'Esd',
            16: u'Ne',
            17: u'Est',
            18: u'Jb',
            19: u'Sal',
            20: u'Pr',
            21: u'Ecl',
            22: u'Ct',
            23: u'Is',
            24: u'Jr',
            25: u'Lm',
            26: u'Ez',
            27: u'Dn',
            28: u'Os',
            29: u'Jl',
            30: u'Am',
            31: u'Ab',
            32: u'Jon',
            33: u'Mi',
            34: u'Na',
            35: u'Ha',
            36: u'So',
            37: u'Hag',
            38: u'Za',
            39: u'Ml',
            40: u'Mt',
            41: u'Mc',
            42: u'Lc',
            43: u'Jn',
            44: u'Hch',
            45: u'Rm',
            46: u'1\u00a0Co',
            47: u'2\u00a0Co',
            48: u'Ga',
            49: u'Ef',
            50: u'Flp',
            51: u'Col',
            52: u'1\u00a0Ts',
            53: u'2\u00a0Ts',
            54: u'1\u00a0Tm',
            55: u'2\u00a0Tm',
            56: u'Tt',
            57: u'Flm',
            58: u'Hb',
            59: u'St',
            60: u'1\u00a0P',
            61: u'2\u00a0P',
            62: u'1\u00a0Jn',
            63: u'2\u00a0Jn',
            64: u'3\u00a0Jn',
            65: u'Jds',
            66: u'Ap'
}
        self._alter_dict()


class THPLASBIndexAbbr(THPBibleTeamAbbr):
    """abbreviations in the LASB Master Index"""
    def __init__(self, nbs=u' ', period=False):
        THPBibleTeamAbbr.__init__(self, nbs=nbs, period=False)
        self.changes = {
            1: u'Gn',
            2: u'Ex',
            3: u'Lv',
            4: u'Nm',
            5: u'Dt',
            6: u'Jos',
            7: u'Jgs',
            8: u'Ru',
            9: u'1\u00a0Sm',
            10: u'2\u00a0Sm',
            15: u'Ezr',
            17: u'Est',
            18: u'Jb',
            20: u'Prv',
            23: u'Is',
            26: u'Ez',
            27: u'Dn',
            29: u'Jl',
            30: u'Am',
            31: u'Ob',
            33: u'Mi',
            34: u'Na',
            35: u'Hab', # Was Hb, but that's not how the NKJV LASB index has it. -GPL
            36: u'Zep',
            37: u'Hg',
            38: u'Zec',
            40: u'Mt',
            41: u'Mk',
            42: u'Lk',
            43: u'Jn',
            54: u'1\u00a0Tm',
            55: u'2\u00a0Tm',
            56: u'Ti',
            60: u'1\u00a0Pt',
            61: u'2\u00a0Pt',
            66: u'Rv',
        }
        self._alter_dict()

class HCSBLASBIndexAbbr(THPLASBIndexAbbr):
    """abbreviations in the LASB Master Index"""
    def __init__(self, nbs=u' ', period=False):
        THPLASBIndexAbbr.__init__(self, nbs=nbs, period=False)
        self.changes = {
            7: u'Jdg',
            11: u'1Kg',
            12: u'2Kg',
            13: u'1Ch',
            14: u'2Ch',
            21: u'Ec',
            22: u'Sg',
            24: u'Jr',
            25: u'Lm',
            26: u'Ezk',
            28: u'Hs',
            32: u'Jnh',
            33: u'Mc',
            38: u'Zch',
            44: u'Ac',
            45: u'Rm',
            46: u'1Co',
            47: u'2Co',
            48: u'Gl',
            50: u'Php',
            52: u'1Th',
            53: u'2Th',
            57: u'Phm',
            59: u'Jms',
            65: u'Jd'
        }
        self._alter_dict()


class THPBibleTeamAbbrDeuterocanon(THPBibleTeamAbbr):
    """The abbreviations used by the Bible team
    for the Deuterocanon"""
    def __init__(self, nbs=u' ', period=False):
        THPBibleTeamAbbr.__init__(self, nbs=u' ')
        self.changes = {
            16.1: u'Tob',
            16.2: u'Jdt',
            17.1: u'1\u00a0Macc',
            17.2: u'2\u00a0Macc',
            22.1: u'Wis',
            22.2: u'Sir',
            25.1: u'Bar',
        }
        self._alter_dict()

class IVPAbbrDeuterocanon(THPBibleTeamAbbrDeuterocanon):
    """Abbreviations used by IVP"""
    def __init__(self, nbs=u' ', period=False):
        THPBibleTeamAbbr.__init__(self, nbs=u' ')
        self.changes = {
            2: u'Ex',
            11: u'1\u00a0Kings',
            12: u'2\u00a0Kings',
            13: u'1\u00a0Chron',
            14: u'2\u00a0Chron',
            17: u'Esther',
            20: u'Prov',
            21: u'Eccles',
            23: u'Is',
            34: u'Nahum',
            40: u'Mt',
            41: u'Mk',
            42: u'Lk',
            43: u'Jn',
            52: u'1\u00a0Thess',
            53: u'2\u00a0Thess',
            54: u'Philem',
            15.1: u'1\u00a0Esdr',
            15.2: u'2\u00a0Esdr',
            17.1: u'Add\u00a0Esther',
            24.1: u'Ep\u00a0Jer',
            27.1: u'Pr\u00a0Azar',
            27.2: u'Sus',
            27.3: u'Bel',
            14.1: u'Pr\u00a0Man',
            17.2: u'1\u00a0Macc',
            17.3: u'2\u00a0Macc',
            17.4: u'3\u00a0Macc',
            17.5: u'4\u00a0Macc',
        }
        self._alter_dict()

class SBLAbbr(THPBibleTeamAbbr):
    """The SBL abbreviations are almost the same as Bible team's"""
    def __init__(self, nbs=u' '):
        THPBibleTeamAbbr.__init__(self, nbs=nbs, period=False)
        self.changes = {
            32: u'Jonah',
            52: u'1\u00a0Thess',
            53: u'2\u00a0Thess',
            62: u'1\u00a0John',
            63: u'2\u00a0John',
            64: u'3\u00a0John',
        }
        self._alter_dict()
        

class SBLAbbrCanticles(SBLAbbr):
    """Canticles instead of Song of Songs"""
    def __init__(self, nbs=u' '):
        SBLAbbr.__init__(self, nbs=nbs)
        self.changes = {
            22: u'Cant',
        }
        self._alter_dict()


class SBLAbbrQoheleth(SBLAbbr):
    """Qoheleth instead of Ecclesiastes"""
    def __init__(self, nbs=u' '):
        SBLAbbr.__init__(self, nbs=nbs)
        self.changes = {
            21: u'Qoh',
        }
        self._alter_dict()

class SBLAbbrDeuterocanon(SBLAbbr):
    """The abbreviations used in SBLHS
    for the Deuterocanon"""
    def __init__(self):
        SBLAbbr.__init__(self, nbs=u' ')
        self.lang = 'en'
        self.changes = {
            16.1: u'Tob',
            16.2: u'Jdt',
            17.1: u'1\u00a0Macc',
            17.2: u'2\u00a0Macc',
            22.1: u'Wis',
            22.2: u'Sir',
            25.1: u'Bar',
        }
        self._alter_dict()


class THPBibleTextAbbr(BookNameSystem):
    """The abbreviations used in THP bibletext repository"""
    def __init__(self):
        BookNameSystem.__init__(self, nbs=u' ')
        self.lang = 'en'
        self.changes = {
            1: u'gene',
            2: u'exod',
            3: u'levi',
            4: u'numb',
            5: u'deut',
            6: u'josh',
            7: u'judg',
            8: u'ruth',
            9: u'sam1',
            10: u'sam2',
            11: u'kgs1',
            12: u'kgs2',
            13: u'chr1',
            14: u'chr2',
            15: u'ezra',
            16: u'nehe',
            17: u'esth',
            18: u'job',
            19: u'psal',
            20: u'prov',
            21: u'eccl',
            22: u'song',
            23: u'isai',
            24: u'jere',
            25: u'lame',
            26: u'ezek',
            27: u'dani',
            28: u'hose',
            29: u'joel',
            30: u'amos',
            31: u'obad',
            32: u'jona',
            33: u'mica',
            34: u'nahu',
            35: u'haba',
            36: u'zeph',
            37: u'hagg',
            38: u'zech',
            39: u'mala',
            40: u'matt',
            41: u'mark',
            42: u'luke',
            43: u'john',
            44: u'acts',
            45: u'roma',
            46: u'cor1',
            47: u'cor2',
            48: u'gala',
            49: u'ephe',
            50: u'phil',
            51: u'colo',
            52: u'the1',
            53: u'the2',
            54: u'tim1',
            55: u'tim2',
            56: u'titu',
            57: u'phlm',
            58: u'hebr',
            59: u'jame',
            60: u'pet1',
            61: u'pet2',
            62: u'joh1',
            63: u'joh2',
            64: u'joh3',
            65: u'jude',
            66: u'reve'
        }
        self._alter_dict()

class THPBibleTextDeuterocanonAbbr(THPBibleTextAbbr):
    """The abbreviations used in THP bibletext repository
    for the Deuterocanon"""
    def __init__(self):
        BookNameSystem.__init__(self, nbs=u' ')
        self.lang = 'en'
        self.changes = {
            16.1: u'tobi',
            16.2: u'judi',
            17.1: u'mac1',
            17.2: u'mac2',
            22.1: u'wisd',
            22.2: u'sira',
            25.1: u'baru',
        }
        self._alter_dict()

class THPXMLAbbr(THPBibleTeamAbbrDeuterocanon):
    """The system used for xml references, in which id's can't start with
    a number. -- MJW
    """
    def __init__(self):
        THPBibleTeamAbbrDeuterocanon.__init__(self, nbs=u' ', period=False)
        # for key in self.book_dict.keys():
        #     print key, self.book_dict[key]
        self.changes = {
            9: u'ISam',
            10: u'IISam',
            11: u'IKgs',
            12: u'IIKgs',
            13: u'IChr',
            14: u'IIChr',
            17.1: u'IMacc',
            17.2: u'IIMacc',
            19: u'Ps',
            37: u'Hagg',
            46: u'ICor',
            47: u'IICor',
            52: u'IThes',
            53: u'IIThes',
            54: u'ITim',
            55: u'IITim',
            60: u'IPet',
            61: u'IIPet',
            62: u'IJn',
            63: u'IIJn',
            64: u'IIIJn',
        }
        self._alter_dict()
        

class BookNameBinder():
    """
    Allows you to activate multiple BookNameSystems at once.
    """
    def __init__(self, book_name_systems=None):
        if book_name_systems == None:
            book_name_systems = [
                    THPFullName(),
                    THPFullName(nbs=u'\u00a0'),
                    THPFullName(nbs=u'<nbs/>'),
                    THPBibleTeamAbbr(),
                    THPBibleTeamAbbr(nbs=u'\u00a0'),
                    THPBibleTeamAbbr(nbs=u'<nbs/>'),
                ]
        self.book_name_systems = book_name_systems
        # print self.book_name_systems

    def book_list(self):
        """
        Return a list of the books in order
        """
        key_value_pairs = []
        for book_name_system in self.book_name_systems:
            key_value_pairs.extend(
                [(key, value) for key, value in book_name_system.book_dict.iteritems()])
        key_value_pairs = sorted(key_value_pairs)#, key=lambda kvp: kvp[0])
        b_list = []
        for kvp in key_value_pairs:
            if kvp[1] not in b_list:
                b_list.append(kvp[1])
        # If Psalms, add Psalm
        if u'Psalms' in b_list:
            b_list.append(u'Psalm')
        if u'Salmos' in b_list:
            b_list.append(u'Salmo')
        return b_list

    def book_name_to_number(self):
        """
        Returns a dictionary with the book name options as keys and numbers as
        values
        """
        key_value_pairs = []
        for book_name_system in self.book_name_systems:
            key_value_pairs.extend(
                [(key, value) for key, value in book_name_system.book_dict.iteritems()])
        key_value_pairs = sorted(key_value_pairs)#, key=lambda kvp: kvp[0])
        name2number = {u'Psalm': 19, u'psalm': 19, u'PSALM': 19,
                        u'Salmo': 19, u'salmo': 19, u'SALMO': 19,}
        for kvp in key_value_pairs:
            if kvp[1] not in name2number:
                name2number[kvp[1]] = kvp[0]
            if kvp[1].upper() not in name2number:
                name2number[kvp[1].upper()] = kvp[0]
            if kvp[1].lower() not in name2number:
                name2number[kvp[1].lower()] = kvp[0]
            # if kvp[1].lower == u'psalms':
            #     name2number[u'psalm'] = kvp[0]
            #     name2number[u'PSALM'] = kvp[0]
            #     name2number[u'Psalm'] = kvp[0]
            # if kvp[1].lower == u'salmos':
            #     name2number[u'salmo'] = kvp[0]
            #     name2number[u'SALMO'] = kvp[0]
            #     name2number[u'Salmo'] = kvp[0]
        return name2number

def tester():
    # all_options = []
    systems = [
        THPFullName(),
        THPFullName(nbs=u'\u00a0'),
        THPTMSAbbr(),
        THPTMSAbbr(nbs=u'\u00a0'),
        THPBibleTeamAbbr(),
        THPBibleTeamAbbr(nbs=u'\u00a0'),
        THPBibleTextAbbr(),
        THPFullNameSongs(),
        THPXMLAbbr(),
        SBLFullNameQoheleth(),
        SBLFullNameCanticles(),
        SBLAbbr(),
        SBLAbbr(nbs=u'\u00a0'),
        SBLAbbrQoheleth(),
        SBLAbbrCanticles(),
        ]
    fl = open(r'C:\Sandbox\all_options.txt', 'w')
    # for system in systems:
    #     all_options.extend(system.book_list())
        #fl.write('\n%s\n%s\n' % (system.__class__.__name__,
        #    '=' * len(system.__class__.__name__)))
        #fl.write('\n'.join(system.book_list()).encode('utf-8'))
    # set_options = set(all_options)
    # all_options = [option for option in set_options]
    # all_options.sort(key = len, reverse=True)
    bnb = BookNameBinder(systems)
    print bnb.book_name_to_number()
    text = '|'.join(bnb.book_list())
    fl.write(text.encode('utf-8'))
    fl.close()

def bk_names_to_spanish(path):
    fl = codecs.open(path, 'r', encoding='utf-8')
    text = fl.read()
    fl.close()
    system1 = THPFullName(nbs=u'\u00a0')
    system2 = THPSpanishFullName(nbs=u'\u00a0')
    for i in range(1, 67):
        text = text.replace(
            u'%s ' % system1.book_dict[i],
            u'%s ' % system2.book_dict[i])
    fl = codecs.open(path, 'w', encoding='utf-8')
    fl.write(text)
    fl.close()


if __name__ == '__main__':
    # tester()
    # bs = THPFullNameDeuterocanon()
    bs = THPBibleTeamAbbrHagg()
    # for key in bs.book_dict.keys():
    #     print '"%s", "%s"' % (str(key), bs.book_dict[key])
    print '|'.join(bs.book_list()).encode('utf-8')
    # bk_names_to_spanish(r'C:\bibles\products\All-Shared\ReadingPlans\PlanDeLectura365.xml')
