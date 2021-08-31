# -*- coding: utf-8 -*-
# Python 3.6.12
"""

"""

from nltk.tokenize import word_tokenize as tokenize

from tqdm import tqdm

def tokenize_file(path, path_out, language, linenumber):
    with open(path, encoding='utf-8') as file_in, \
         open(path_out, 'w', encoding='utf-8') as file_out:
        for line in tqdm(file_in, total=linenumber, desc='Tokenization'):
            tokens = tokenize(line, language)
            file_out.write(' '.join(tokens) + '\n')


if __name__ == '__main__':
    SRC_FILE = 'de-en/europarl-v7.de-en.de'
    TGT_FILE = 'de-en/europarl-v7.de-en.en'
    SRC_FILE_TOKENIZED = 'giza-pp/europarl_data/Source'
    TGT_FILE_TOKENIZED = 'giza-pp/europarl_data/Target'
    LINENUMBER = 1920210

    tokenize_file(SRC_FILE, SRC_FILE_TOKENIZED, 'german', LINENUMBER)
    tokenize_file(TGT_FILE, TGT_FILE_TOKENIZED, 'english', LINENUMBER)
