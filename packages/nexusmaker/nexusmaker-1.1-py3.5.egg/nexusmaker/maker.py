import codecs
from collections import defaultdict
from functools import lru_cache

from nexus import NexusWriter, NexusReader

from .CognateParser import CognateParser
from .tools import slugify

class Record(object):
    def __init__(self,
        ID=None, LID=None, WID=None, Language=None, Word=None, Item=None,
        Annotation=None, Loan=None, Cognacy=None
    ):
        self.ID = ID
        self.LID = LID
        self.WID = WID
        self.Language = Language
        self.Word = Word
        self.Item = Item
        self.Annotation = Annotation
        self.Loan = Loan
        self.Cognacy = Cognacy
    
    def __repr__(self):
        return "<Record %s - %s - %s - %s>" % (self.ID, self.Language, self.Word, self.Item)
    
    @property
    def is_loan(self):
        if self.Loan is None:
            return False
        elif self.Loan in (False, ""):
            return False
        elif self.Loan is True:
            return True
        else:
            return True
    

class NexusMaker(object):
    
    def __init__(self, data, cogparser=CognateParser(strict=True, uniques=True), remove_loans=True):
        self.data = [self._check(r) for r in data]
        
        self.cogparser = cogparser
        
        # loan words
        self.remove_loans = remove_loans
        if self.remove_loans:
            self.data = [r for r in data if not r.is_loan]
        
    def _check(self, record):
        """Checks that all records have the keys we need"""
        if getattr(record, 'Language', None) is None:
            raise ValueError("record has no `Language` %r" % record)
        if getattr(record, 'Word', None) is None:
            raise ValueError("record has no `Word` %r" % record)
        return record
    
    @lru_cache(maxsize=None)
    def _is_missing_for_word(self, language, word):
        """Returns True if the given `language` has no cognates for `word`"""
        for cog in [c for c in self.cognates if c[0] == word]:
            if language in self.cognates[cog]:
                return False
        return True
        
    @property
    def languages(self):
        if not hasattr(self, '_languages'):
            self._languages = {r.Language for r in self.data}
        return self._languages
        
    @property
    def words(self):
        if not hasattr(self, '_words'):
            self._words = {r.Word for r in self.data}
        return self._words
    
    @property
    def cognates(self):
        if not hasattr(self, '_cognates'):
            self._cognates, self._uniques = {}, set()
            for rec in self.data:
                if self.remove_loans and rec.is_loan:
                    raise ValueError("%r is a loan word!")
                
                for cog in self.cogparser.parse_cognate(rec.Cognacy):
                    # don't add multiple uniques for each language-word combination
                    if self.cogparser.UNIQUE_IDENTIFIER in cog:
                        if (rec.Language, rec.Word) in self._uniques:
                            continue
                        self._uniques.add((rec.Language, rec.Word))
                    # add cognate
                    coglabel = (rec.Word, cog)
                    self._cognates[coglabel] = self._cognates.get(coglabel, set())
                    self._cognates[coglabel].add(rec.Language)
        return self._cognates
    
    def make(self):
        nex = NexusWriter()
        for cog in self.cognates:
            if self.cogparser.UNIQUE_IDENTIFIER in cog:
                assert len(self.cognates[cog]) == 1
            else:
                assert len(self.cognates[cog]) >= 1, "%s = %r" % (cog, self.cognates[cog])
            
            for lang in self.languages:
                if lang in self.cognates[cog]:
                    value = '1'
                elif self._is_missing_for_word(lang, cog[0]):
                    value = '?'
                else:
                    value = '0'
                print("Add: ", slugify(lang), slugify("_".join(cog)), value)
                nex.add(slugify(lang), slugify("_".join(cog)), value)
        nex.write_to_file('_temp.nex', charblock=True)
        nex = self._add_ascertainment(nex)  # handle ascertainment
        return nex
    
    def _add_ascertainment(self, nex):
        # subclass this to extend
        return nex
    
    def display_cognates(self):  # pragma: no cover
        for cog in sorted(self.cognates):
            print(cog, sorted(self.cognates[cog]))
    
    def write(self, nex=None, filename=None):
        if nex is None:
            nex = self.make()
        
        if filename is None:
            return nex.write(charblock=True)
        else:
            return nex.write_to_file(filename=filename, charblock=True)
        
        
        
class NexusMakerAscertained(NexusMaker):
    
    OVERALL_ASCERTAINMENT_LABEL = '_ascertainment_0'
    
    def _add_ascertainment(self, nex):
        """Adds an overall ascertainment character"""
        if self.OVERALL_ASCERTAINMENT_LABEL in nex.data:
            raise ValueError('Duplicate ascertainment key %s!' % self.OVERALL_ASCERTAINMENT_LABEL)
            
        for lang in self.languages:
            nex.add(lang, self.OVERALL_ASCERTAINMENT_LABEL, '0')
        return nex


class NexusMakerAscertainedWords(NexusMaker):
    
    def _add_ascertainment(self, nex):
        """Adds an ascertainment character per word"""
        for word in self.words:
            coglabel = '%s_0' % word
            if coglabel in nex.data:
                raise ValueError('Duplicate ascertainment key %s!' % coglabel)
            
            for lang in self.languages:
                if self._is_missing_for_word(lang, word):
                    nex.add(lang, coglabel, '?')
                else:
                    nex.add(lang, coglabel, '0')
        return nex
    
    def _get_characters(self, nex, delimiter="_"):
        """Find all characters"""
        chars = defaultdict(list)
        for site_id, label in enumerate(sorted(nex.data.keys())):
            if delimiter in label:
                word, cogid = label.rsplit(delimiter, 1)
            else:
                raise ValueError("No delimiter %s in %s" % (delimiter, label))
            chars[word].append(site_id)
        return chars

    def _is_sequential(self, siteids):
        return sorted(siteids) == list(range(min(siteids), max(siteids)+1))

    def create_assumptions(self, nex):
        chars = self._get_characters(nex)
        buffer = []
        buffer.append("begin assumptions;")
        for char in sorted(chars):
            siteids = sorted(chars[char])
            # increment by one as these are siteids not character positions
            siteids = [s+1 for s in siteids]
            assert self._is_sequential(siteids), 'char is not sequential %s' % char
            if min(siteids) == max(siteids):
                out = "\tcharset %s = %d;" % (char, min(siteids))
            else:
                out = "\tcharset %s = %d-%d;" % (char, min(siteids), max(siteids))
            buffer.append(out)
        buffer.append("end;")
        return buffer

    def write(self, nex=None, filename=None):
        if nex is None:
            nex = self.make()
        
        if filename is None:
            return nex.write(charblock=True) + "\n\n" + "\n".join(self.create_assumptions(nex))
        else:  # pragma: no cover
            nex.write_to_file(filename=filename, charblock=True)
            with open(filename, 'a', encoding='utf8') as handle:
                handle.write("\n")
                for line in self.create_assumptions(nex):
                    handle.write(line + "\n")
                handle.write("\n")
            return True
