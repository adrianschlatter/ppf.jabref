#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools to work with JabRef database.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, VARCHAR, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
import re
from .utils import export


Base = declarative_base()


@export
def citationkey2counter(citationkey):
    # 'a': 0, 'b': 1, ..., 'z': 25
    # 'aa': 26, 'ab': 27
    # 'aaa': 26 + 26**2 + 0, 'aab': 26 + 26**2 + 1

    # Let n = len(citationkey).
    # Then first count all keys used by keys of length <n:
    counter = 0
    for i in range(1, len(citationkey)):
        counter += 26**i

    # Then, add position of citationkey within keys of length n:
    for i, c in enumerate(citationkey[::-1]):
        digit = ord(c) - ord('a')
        counter += digit * 26 ** i

    return counter


@export
def counter2citationkey(counter):
    n = 1
    while(True):
        if counter < 26 ** n:
            break

        counter -= 26 ** n
        n += 1

    citationkey = ['z'] * n
    for i in range(n)[::-1]:
        digit = counter // 26 ** i
        counter = counter % 26 ** i
        citationkey[-i - 1] = chr(digit + ord('a'))

    return ''.join(citationkey)


@export
class Entry(Base):
    """Represent a JabRef Entry."""

    __tablename__ = 'ENTRY'

    shared_id = Column('SHARED_ID', Integer, primary_key=True)
    type = Column(VARCHAR(255), nullable=False)
    version = Column(Integer, nullable=True)
    _fields = relationship(
        'Field',
        collection_class=attribute_mapped_collection('name'))

    # Access like entry.fields['author'] returns 'A. Muller'
    # which is nicer than using enttry.fields['author'].value:
    fields = association_proxy('_fields', 'value')


@export
class Field(Base):
    """Represent a JabRef Field."""

    __tablename__ = 'FIELD'

    entry_shared_id = Column(Integer, ForeignKey('ENTRY.SHARED_ID'),
                             primary_key=True)
    name = Column(VARCHAR(255), primary_key=True)
    value = Column(Text, nullable=True)


@export
def split_by_unescaped_sep(text, sep=':'):
    """Split string at sep but only if not escaped."""
    def remerge(s):
        # s is a list of strings.
        for i in range(len(s) - 1):
            n_esc = len(s[i]) - len(s[i].rstrip('\\'))
            if n_esc % 2 == 0:
                continue
            else:
                new_s = s[:i] + [s[i] + sep + s[i + 1]] + s[i + 2:]
                return remerge(new_s)
        return s

    # split by every sep (even unescaped ones)
    # then re-merge strings that end in an uneven number of escape chars:
    return remerge(text.split(sep))


@ export
class Link():
    """A JabRef link as used to link to files and URLs."""

    def __init__(self, name, path, filetype):
        self.name, self.path, self.filetype = name, path, filetype

    def __repr__(self):
        """Return string representation."""
        return ':'.join([Link.escape(s)
                         for s in [self.name, self.path, self.filetype]])

    @ classmethod
    def from_string(cls, string):
        """Alternative constructor to create Link from JabRef link string."""
        name, path, filetype = [cls.unescape(part) for part
                                in split_by_unescaped_sep(string, sep=':')]
        return cls(name, path, filetype)

    @ staticmethod
    def escape(s):
        """Escape string s."""
        escaped = re.sub(r'\\', r'\\\\', s)
        escaped = re.sub(':', r'\:', escaped)
        escaped = re.sub(';', r'\;', escaped)
        return escaped

    @ staticmethod
    def unescape(text):
        r"""
        Unescape string s.

        Assumes that there are no unescaped \, ;, ; in s.
        """
        text = re.sub(r'\\;', ';', text)
        text = re.sub(r'\\:', ':', text)
        text = re.sub(r'\\\\', r'\\', text)
        return text


@export
class File():
    r"""
    Represent a JabRef File entry.

    A JabRef File entry is a ;-separated list of links. Each link is
    a :-separated list of name, path, and type. Each field is an escaped
    string (escape char is \, chars that need escaping are :, ;, and \).

    Example: 'Preface:Books\\Preface.pdf:PDF;Chapter 1:Books\\Chapter1.pdf:PDF'
    """

    def __init__(self, list_of_links):
        for link in list_of_links:
            if type(link) is not Link:
                raise TypeError(f'{link} is not a Link')
        self._links = list_of_links

    def __repr__(self):
        return ';'.join([str(link) for link in self._links])

    @classmethod
    def from_string(cls, string):
        """Create File from JabRef File entry."""
        links = split_by_unescaped_sep(string, ';')
        return cls([Link.from_string(link) for link in links])

    def __getitem__(self, key):
        return self._links[key]

    def __len__(self):
        return len(self._links)
