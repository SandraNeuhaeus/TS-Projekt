# Python: 3.7.6
# Kodierung: utf-8

"""Dieses Modul verwendet die Ergebnisse aus Schritt 2 für Schritt 1.

Alignierung bei Aussonderung von Nicht-Konnektor-Lesarten.

"""
import logging

from tqdm import tqdm

from disambiguator import Disambiguator as da
from list_aligner import ListAligner
from split_text import token_split


class DisambigAligner(ListAligner):
    """Combines the disambiguation and the alignment."""

    def __init__(self, src_connectors, tgt_connectors):
        super().__init__(src_connectors, tgt_connectors)

    def align(self, src_path, tgt_path, frame=33, start=-16, max_window=0):
        """Performs a disambiguation before list alignment.

        Args:
            src_path(str): Path to the file in the source language (the
                           same as self.connectors).
            tgt_path(str): Path to the target file, where we're trying to
                           find equivalents of the connectors in the source
                           file.
            frame(int): Size of the frame in which an equivalent in searched.
            start(int): A negative value that states the position of the first
                        token in the frame relative to the source connector.
            max_window(int): Maximum connector length that is searched for. If
                             None, the maximum length is computed from
                             'self.tgt_connectors'.

        """
        alignments = dict()
        not_occs = da.create_non_con_dict(self.src_connectors, src_path)[0]
        occs = dict()
        if not max_window:
            max_window = self._compute_maxwindow()
        with open(src_path, encoding='utf-8') as src_file, \
             open(tgt_path, encoding='utf-8') as tgt_file:
            lineno = 1
            pbar = tqdm(total=1920209, desc='Matching connectors')
            while True:
                try:
                    src_line = next(src_file).casefold()
                    tgt_line = next(tgt_file).casefold()
                except StopIteration:
                    break
                src_tokens = token_split(src_line)
                tgt_tokens = token_split(tgt_line)
                token_id = 0
                # It may happen that a target connector is matched twice.
                for token in src_tokens:
                    if token in self.src_connectors:
                        if token not in occs:
                            occs[token] = 0
                        else:
                            occs[token] += 1
                        if token in not_occs:
                            if occs[token] in not_occs[token]:
                                continue
                        equivalent = self._search_equivalent(
                                tgt_tokens, token_id,
                                frame, start, max_window
                                )
                        # Add equivalent to alignments.
                        self.note_match(alignments, token, equivalent)
                        if not equivalent:
                            logging.info(f'No match: Line {lineno} ({token})')
                    token_id += 1
                lineno += 1
                pbar.update(1)
            pbar.close()
        return alignments


def main():
    logging.basicConfig(filename="results/disambig/no_matches.log",
                        filemode='w', level=logging.INFO)
    obj1 = DisambigAligner(
            src_connectors={'aber', 'doch', 'jedoch',
                            'allerdings', 'andererseits', 'hingegen'},
            tgt_connectors={'but', 'however', 'though',
                            'although', 'yet', 'nevertheless',
                            'nonetheless', 'albeit', 'otherwise',
                            'whereas', 'again', 'still', 'instead',
                            'alternatively', 'after all', 'then again',
                            'there again', 'by contrast', 'on the contrary',
                            'on the other hand', 'at the same time',
                            'even so', 'even if', 'by the same token',
                            'on a different note', 'on the other side',
                            'on the downside', 'having said this',
                            'having said that', 'apart from that'}
            )
    europarl_result = obj1.align('de-en/europarl-v7.de-en.de',
                                 'de-en/europarl-v7.de-en.en')
    # Save results df to csv.
    europarl_df = obj1.result_to_df(
            europarl_result, save='results/disambig/disambig_33_minus16.csv'
            )
    # Save top 10 matches for every connector.
    obj1.print_top_values(
            europarl_df, save='results/disambig/disambig_33_minus16.txt'
            )


if __name__ == "__main__":
    main()
