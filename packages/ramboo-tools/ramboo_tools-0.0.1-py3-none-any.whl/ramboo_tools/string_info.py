#!/usr/bin/env python
# -*- coding: utf8 -*-

# 系统库
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import sys

# 第三方库
import unicodedata

__all__ = ['UnicodeCategory', 'StringInfo']
PY3K = sys.version_info[0] >= 3
if PY3K:
    unicode_type = str
else:
    unicode_type = unicode


class UnicodeCategory(object):
    """
    General Category for Unicode
    http://www.unicode.org/versions/Unicode6.0.0/ch04.pdf
    """

    # Letter
    UppercaseLetter = 'Lu'
    LowercaseLetter = 'Ll'
    TitlecaseLetter = 'Lt'
    ModifierLetter = 'Lm'
    OtherLetter = 'Lo'
    # Mark
    NonSpacingMark = 'Mn'
    SpacingCombiningMark = 'Mc'
    EnclosingMark = 'Me'
    # Number
    DecimalDigitNumber = 'Nd'
    LetterNumber = 'Nl'
    OtherNumber = 'No'
    # Separator
    SpaceSeparator = 'Zs'
    LineSeparator = 'Zl'
    ParagraphSeparator = 'Zp'
    # Punctuation
    ConnectorPunctuation = 'Pc'
    DashPunctuation = 'Pd'
    OpenPunctuation = 'Ps'
    ClosePunctuation = 'Pe'
    InitialQuotePunctuation = 'Pi'
    FinalQuotePunctuation = 'Pf'
    OtherPunctuation = 'Po'
    # Symbol
    MathSymbol = 'Sm'
    CurrencySymbol = 'Sc'
    ModifierSymbol = 'Sk'
    OtherSymbol = 'So'
    # Other
    Control = 'Cc'
    Format = 'Cf'
    Surrogate = 'Cs'
    PrivateUse = 'Co'
    OtherNotAssigned = 'Cn'


class StringInfo(object):
    """
    字符串信息
    """

    def __init__(self, s):
        if not isinstance(s, unicode_type):
            raise TypeError("'string' parameter must be unicode")
        self.s = s

    @property
    def length_in_text_elements(self):
        """Gets the number of text elements."""
        l = getattr(self, '_length_in_text_elements', None)
        if l is None:
            l = sum(1 for _ in self.text_element_length_generator(self.s))
            setattr(self, '_length_in_text_elements', l)
        return l

    @classmethod
    def text_element_length_generator(cls, s):
        """Gets the text element index generator of the specified string."""
        if not isinstance(s, unicode_type):
            raise TypeError("parameter 's' must be unicode")
        marks = set([UnicodeCategory.NonSpacingMark, UnicodeCategory.SpacingCombiningMark, UnicodeCategory.EnclosingMark])
        idx = 0
        while idx < len(s):
            ch = s[idx]
            count = 1
            cat = unicodedata.category(ch)
            if cat == UnicodeCategory.Surrogate:
                # Check that it's a high surrogate followed by a low surrogate
                if 0xD800 <= ord(ch) <= 0xDBFF:
                    if (idx + 1) < len(s) and 0xDC00 <= ord(s[idx + 1]) <= 0xDFFF:
                        # A valid surrogate pair
                        count = 2
            else:
                # Look for a base character, which may or may not be followed by a
                # series of combining characters
                if cat not in marks:
                    while idx + count < len(s):
                        cat = unicodedata.category(s[idx + count])
                        if cat not in marks:
                            # Finished the sequence
                            break
                        count += 1
            yield count
            idx += count

    @classmethod
    def text_element_generator(cls, s):
        """Gets the text element generator of the specified string."""
        idx = 0
        for length in cls.text_element_length_generator(s):
            yield s[idx : idx + length]
            idx += length
