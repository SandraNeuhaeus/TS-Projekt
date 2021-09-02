# -*- coding: utf-8 -*-
# Python 3.6.12

"""Prepares the data files to run Giza."""


from nltk.tokenize import word_tokenize as tokenize

from tqdm import tqdm


def tokenize_file(path, path_out, language, linenumber=None):
    """Tokenizes a file.

    Args:
        path (str): Path to input file (.txt) that should be tokenized.
        path_out (str): Path to tokenized output file (.txt).
        language (str): The language the text is written in.
        linenumber (int): Number of lines in input file. If None, the
                          program can't compute the remaining duration
                          of the tokenization.

    """
    with open(path, encoding='utf-8') as file_in, \
         open(path_out, 'w', encoding='utf-8') as file_out:
        for line in tqdm(file_in, total=linenumber,
                         desc='Tokenization of a file'):
            tokens = tokenize(line, language)
            file_out.write(' '.join(tokens) + '\n')


if __name__ == '__main__':
    SRC_FILE = '../de-en/europarl-v7.de-en.de'
    TGT_FILE = '../de-en/europarl-v7.de-en.en'
    SRC_FILE_TOKENIZED = 'giza-pp/europarl_data/Source'
    TGT_FILE_TOKENIZED = 'giza-pp/europarl_data/Target'
    LINENUMBER = 1920210

    tokenize_file(SRC_FILE, SRC_FILE_TOKENIZED, 'german', LINENUMBER)
    tokenize_file(TGT_FILE, TGT_FILE_TOKENIZED, 'english', LINENUMBER)
