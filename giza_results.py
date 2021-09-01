# -*- coding: utf-8 -*-
# Python 3.6.12

"""Extracts information about specified words from the Giza results."""


import pandas as pd

from tqdm import tqdm

from abstract_aligner import Aligner

class GizaResultsReader():
    """Extracts Giza alignments for given connectors.

    Attributes:
        src_connectors (set): A set of words for which all alignments are
                              counted.
        alignments (dict): Contains the aligned connectors. Has the form:
            {<source_connector1>: {
                        <target_connector1>: <number_of_matches>,
                        ...}
                ...
                }

    """
    def __init__(self, src_connectors):
        self.src_connectors = src_connectors
        self.alignments = dict()

    def read_results(self, resultsfile):
        """Extracts specified alignments from the Giza results.

        Finds the results for the words in the set
        'self.src_connectors'.

        Args:
            resultsfile (str): Path to file that contains Giza's results.

        Returns:
            dict: The aligned connectors. Has the form:
                {<source_connector1>: {
                        <target_connector1>: <number_of_matches>,
                        ...}
                ...
                }

        """
        alignments = dict()
        with open(resultsfile, encoding='utf-8') as results:
            for line in tqdm(results, desc='Reading Giza results',
                             total=1908920*3):
                if line.startswith('#'):
                    continue
                elif not line.startswith('NULL'):
                    english_toks = line.split(' ')
                else:
                    tokens = line.split(' ')
                    i = 0
                    while i < len(tokens):
                        if tokens[i] in self.src_connectors:
                            connector = tokens[i]
                            # tokens[i+1] is '({'. tokens[i+2] is
                            # a number or '})' if there is no match.
                            i += 2
                            # Join equivalents that consist of
                            # multiple words to one string.
                            equivalent_toks = []
                            while tokens[i].isnumeric():
                                equivalent_toks.append(
                                        english_toks[int(tokens[i]) - 1]
                                        )
                                i += 1
                            equivalent = ' '.join(equivalent_toks)
                            Aligner.note_match(alignments,
                                               connector,
                                               equivalent)
                        i += 1
        return alignments


def main():
    obj = GizaResultsReader({'aber', 'doch', 'jedoch',
                             'allerdings', 'andererseits', 'hingegen'})
    giza_result = obj.read_results(
            'giza-pp/europarl_data/output/Result.A3.final')

    # Save results to csv.
    giza_df = Aligner.result_to_df(giza_result, save='results/giza.csv')

    # Save top matches of every connector.
    Aligner.print_top_values(giza_df, save='results/giza.txt', top=15)


if __name__ == '__main__':
    main()
