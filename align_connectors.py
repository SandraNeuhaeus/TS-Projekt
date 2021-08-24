#      Python: 3.7.6
#   Kodierung: utf-8
"""Dieses Modul fasst Funktionalitäten zur Alignierung von Wörtern zusammen.

Es soll den ersten Schritt des Modulprojekts erfüllen.

"""
from split_text import token_split
import numpy as np
import pandas as pd


class Aligner():
    """Produces mappings from certain words in one text to another text."""

    def __init__(self, connectors, mode='naive'):
        #: list of str: contains the tokens supposedly contained in the source
        #               that are mapped to tokens in the target text.
        self.connectors = connectors
        #: obj:'str', optional: determines the alignment algorithm applied.
        self.mode = mode

    def align(self, src_path, tgt_path):
        """Aims to align the connectors from two text files.

        Args:
            src_path(str): directory of the file in the source language (the
                           same as self.connectors).
            tgt_path(str): directory of the target file, where we're trying to
                           find equivalents of the connectors in the source
                           file.

        """
        if self.mode == 'naive':
            return self.__naive_align(src_path, tgt_path)

    def __naive_align(self, src_path, tgt_path):
        """Maps source text tokens (in self.connectors) to target text tokens.

        In the general case tokens with the same index are matched:

            src_tokens: [-, -, =, -]
                               |
                               V
            tgt_tokens: [-, -, =, -]

        When there are less tgt_tokens than src_tokens and there is no token
        in the tgt_tokens at the index of the connector we distinguish two
        cases:
        1.: there are no tgt_tokens and we align with the empty string:

            src_tokens: [-, -, =, -]
                              /
                             /
                            /
                           /
                          /
                         V
            tgt_tokens: [ε]

        2.: tgt_tokens contains tokens but there is no token at the index of
            the connector. In this case we align with the token furthest to
            the right:

            src_tokens: [-, -, -, =]
                                 /
                                /
                               /
                              /
                             /
                            V
            tgt_tokens: [-, =]
        
        Args:
            src_path(str): see Aligner.align().
            tgt_path(str): see Aligner.align().

        Returns:
            alignments(dict): tokens from the source text (str) as keys and
                              dictionaries (dict) as values, that have the
                              matched tokens from the target text (str) for
                              keys and the corresponding number of matches
                              (int) for values.

        """
        alignments = dict()
        src_file = open(src_path, encoding='utf-8')
        tgt_file = open(tgt_path, encoding='utf-8')
        while True:
            try:
                src_line = next(src_file).casefold()
                tgt_line = next(tgt_file).casefold()
            except StopIteration:
                break
            src_tokens = token_split(src_line)
            tgt_tokens = token_split(tgt_line)
            token_id = 0
            for token in src_tokens:
                if token in self.connectors:
                    # target line shorter than source line.
                    if token_id >= len(tgt_tokens):
                        # target line empty.
                        if not tgt_tokens:
                            equivalent = ''
                        else:
                            equivalent = tgt_tokens[-1]
                    else:
                        equivalent = tgt_tokens[token_id]
                    # connector hasn't been aligned yet.
                    if token not in alignments:
                        alignments[token] = {equivalent: 1}
                    # connector hasn't been aligned to equivalent yet.
                    elif equivalent not in alignments[token]:
                        alignments[token][equivalent] = 1
                    # connector has been aligned to equivalent
                    # before.
                    else:
                        alignments[token][equivalent] += 1
                token_id += 1
        src_file.close()
        tgt_file.close()
        return alignments

    @staticmethod
    def result_to_df(d, save=''):
        """Creates a pandas.DataFrame from a nested dictionary.

        Args:
            d(dict): a nested dictionary with immutable keys and dictionaries
                     (dict) as values.
            save(:obj:`str`, optional): path to the .csv-file the DataFrame
                                        can optionally be saved in, if save is
                                        evaluated as True.

        """
        df = pd.DataFrame(d)
        df = df.replace(to_replace=np.nan, value=0)
        df = df.astype(int)
        if save:
            df.to_csv(path_or_buf=save, encoding='utf-8')
        return df


def main():
    obj1 = Aligner({'aber', 'doch', 'jedoch',
                    'allerdings', 'andererseits', 'hingegen'})
    test_result = obj1.align('test.de', 'test.en')
    print(Aligner.result_to_df(test_result))
    europarl_result = obj1.align('de-en/europarl-v7.de-en.de',
                                 'de-en/europarl-v7.de-en.en')
    print(Aligner.result_to_df(europarl_result, save='naive.csv'))
    europarl_df = pd.read_csv('naive.csv', index_col=0)
    for col in europarl_df:
        print(europarl_df.sort_values(by=col, ascending=False).head(10))


if __name__ == "__main__":
    main()
