#!/usr/bin/env python
#
# Simple interface to urbandictionary.com
#
# Author: Roman Bogorodskiy <bogorodskiy@gmail.com>

import sys

if sys.version < '3':
    from urllib import quote as urlquote
    from urllib2 import urlopen
    from HTMLParser import HTMLParser
else:
    from urllib.request import urlopen
    from urllib.parse import quote as urlquote
    from html.parser import HTMLParser


class TermType(object):
    pass


class TermTypeRandom(TermType):
    pass


class UrbanDictParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._section = None
        self.translations = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag not in ('div', 'a', 'span'):
            return

        div_classes = set(attrs_dict.get('class', '').split(' '))
        if div_classes == ['']:
            return
        known_classes = set(
            ('def-header', 'meaning', 'example', 'word', 'category')
        )
        matching_classes = div_classes & known_classes
        if len(matching_classes) == 1:
            self._section = matching_classes.pop()
            if self._section == 'def-header':
                # NOTE: assume 'word' is the first section
                self.translations.append(
                    {'word': '', 'def': '', 'example': '', 'category': ''})

    def handle_endtag(self, tag):
        if tag in ('div', 'a', 'span'):
            # NOTE: assume there is no nested <div> in the known sections
            self._section = None

    def handle_data(self, data):
        if not self._section or self._section == 'def-header':
            return

        if self._section == 'meaning':
            self._section = 'def'
        elif self._section in ('category', 'word'):
            data = data.strip()

        self.translations[-1][self._section] += normalize_newlines(data)


def normalize_newlines(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')


def define(term):
    if isinstance(term, TermTypeRandom):
        url = "http://www.urbandictionary.com/random.php"
    else:
        url = "http://www.urbandictionary.com/define.php?term=%s" % \
              urlquote(term)

    f = urlopen(url)
    data = f.read()
    if hasattr(data, 'decode'):
        data = data.decode('utf-8')

    urbanDictParser = UrbanDictParser()
    urbanDictParser.feed(data)

    return urbanDictParser.translations
