#    Python: 3.7.6
# Kodierung: utf-8
"""Dieses Modul enthält nur eine benutzerdefinierte Tokenisierungfunktion."""
import re


def token_split(s):
    """Auxilary function for tokenizing strings.

    Punctuation marks are completely disregarded.

    Args:
        s(str): the string to be tokenized.

    Returns:
        tokens(:obj:'list' of :obj:'str'): the tokenized string.

    """
    seps = re.compile(r"\s|\.|,|/|\:|\?|!")
    tokens = [token for token in re.split(seps, s) if token]
    return tokens


def main():
    print(token_split('Aber i bim doch a deitscher!'))


if __name__ == "__main__":
    main()
