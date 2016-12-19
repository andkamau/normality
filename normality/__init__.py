import six

from normality.cleaning import collapse_spaces, category_replace
from normality.constants import UNICODE_CATEGORIES
from normality.transliteration import latinize_text, ascii_text
from normality.encoding import guess_encoding  # noqa

WS = ' '


def normalize(text, lowercase=True, collapse=True, latinize=False, ascii=False,
              replace_categories=UNICODE_CATEGORIES):
    """The main normalization function for text.

    This will take a string and apply a set of transformations to it so
    that it can be processed more easily afterwards. Arguments:

    * ``lowercase``: not very mysterious.
    * ``collapse``: replace multiple whitespace-like characters with a
      single whitespace. This is especially useful with category replacement
      which can lead to a lot of whitespace.
    * ``decompose``: apply a unicode normalization (NFKD) to separate
      simple characters and their diacritics.
    * ``replace_categories``: This will perform a replacement of whole
      classes of unicode characters (e.g. symbols, marks, numbers) with a
      given character. It is used to replace any non-text elements of the
      input string.
    """
    if not isinstance(text, six.string_types):
        return

    # TODO: Python 3?
    if six.PY2 and not isinstance(text, six.text_type):
        encoding = guess_encoding(text, 'utf-8')
        text = text.decode(encoding)

    if lowercase:
        # Yeah I made a Python package for this.
        text = text.lower()

    if ascii:
        # A stricter form of transliteration that leaves only ASCII
        # characters.
        text = ascii_text(text)
    elif latinize:
        # Perform unicode-based transliteration, e.g. of cyricllic
        # or CJK scripts into latin.
        text = latinize_text(text)

    # Perform unicode category-based character replacement. This is
    # used to filter out whole classes of characters, such as symbols,
    # punctuation, or whitespace-like characters.
    text = category_replace(text, replace_categories)

    if collapse:
        # Remove consecutive whitespace.
        text = collapse_spaces(text)

    return text


def slugify(text, sep='-'):
    """A simple slug generator."""
    text = normalize(text, ascii=True)
    if text is not None:
        return text.replace(' ', sep)
