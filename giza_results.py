# -*- coding: utf-8 -*-
# Python 3.6.12

"""Given a list of words, extracts their alignments from the Giza results."""


import pandas as pd

from tqdm import tqdm

from align_connectors import Aligner


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
        """Extracts their alignments from the Giza results.

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
                            self._note_match(connector, equivalent)
                        i += 1
        return self.alignments

    def _note_match(self, connector, equivalent):
        """Enters new found matches to 'self.alignments'.

        Args:
            connector(str): Source connector.
            equivalent(str): Found target connector.

        """
        if connector not in self.alignments:
            self.alignments[connector] = {equivalent: 1}
            # connector hasn't been aligned to equivalent yet.
        elif equivalent not in self.alignments[connector]:
            self.alignments[connector][equivalent] = 1
            # connector has been aligned to equivalent
            # before.
        else:
            self.alignments[connector][equivalent] += 1


def main():
    results_obj = GizaResultsReader({'aber', 'doch', 'jedoch',
                                     'allerdings', 'andererseits', 'hingegen'})
    results_obj.read_results('giza-pp/europarl_data/output/Result.A3.final')
    Aligner.result_to_df(results_obj.alignments, save='results/giza.csv')

    # Save top matches of every connector.
    europarl_df = pd.read_csv('results/giza.csv', index_col=0)
    with open('results/giza.txt',
              'w', encoding='utf-8') as results:
        print('Top 15 of every connector', file=results, end='\n\n')
        for col in europarl_df:
            print(europarl_df[col].sort_values(ascending=False).head(15),
                  file=results, end='\n\n')


if __name__ == '__main__':
    main()
