# -*- coding: utf-8 -*-
# Python 3.6.12

"""This module contains the list alignment approach.

Specified source connectors are matched with specified target
connectors using their distance in the parallel sentences.

"""
import logging

from tqdm import tqdm

from abstract_aligner import Aligner
from split_text import token_split


class ListAligner(Aligner):
    def __init__(self, src_connectors, tgt_connectors):
        self.src_connectors = src_connectors
        self.tgt_connectors = tgt_connectors

    def align(self, src_path, tgt_path, frame=33, start=-16, max_window=None):
        """Aims to align the connectors from two text files.

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
        if not max_window:
            max_window = self._compute_maxwindow()
        return self.__list_align(
                src_path, tgt_path,
                frame, start, max_window
                )

    def _compute_maxwindow(self):
        """Computes the maximum target connector length."""
        max_window = 1
        for connector in self.tgt_connectors:
            window = len(connector.split(" "))
            if window > max_window:
                max_window = window
        return max_window

    def __list_align(self, src_path, tgt_path, frame, start, max_window):
        """Uses a list of target connectors to align the source connectors.

        Args:
            src_path(str): directory of the file in the source language (the
                           same as self.connectors).
            tgt_path(str): directory of the target file, where we're trying to
                           find equivalents of the connectors in the source
                           file.
            frame(int): Size of the frame in which an equivalent in searched.
            start(int): A negative value that states the position of the first
                        token in the frame relative to the source connector.
            max_window(int): Maximum connector length that is searched for.

        Returns:
            dict: The aligned connectors. Has the form:
                {<source_connector1>: {
                        <target_connector1>: <number_of_matches>,
                        ...}
                ...
                }

        """
        alignments = dict()
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

    def _search_equivalent(self, tokens, entry, frame, start, max_window):
        """Searches for connectors from 'self.tgt_connectors' in a token list.

        Starts at index 'entry' in the token list, then searches step by
        step at farther positions. Starts with one-word connectors, then
        two-word connectors etc.

        Args:
            tokens(list): A tokenized sentence.
            entry(int): Index of the connector from the source sentence.
            frame(int): Size of the frame in which an equivalent is searched.
            start(int): A negative value that states the position of the first
                        token in the frame relative to 'entry'.
            max_window(int): Maximum connector length that is searched for.

        Returns:
            str: The found equivalent. If no equivalent is found, empty string.

        """
        if not tokens:
            return ''
        first = entry + start
        last = entry + start + frame
        sent_length = len(tokens)
        if first < 0:
            first = 0
        if last > sent_length:
            last = sent_length
        # Annahme: entry als Startpunkt (muss im Fenster liegen)
        # a = negative Größe des Slices (für linke Intervallgrenze)
        for a in range(-1, -(max_window+1), -1):
            pos = iter(range(1, frame))
            non_pos = iter(range(0, -frame, -1))
            # Geht's links noch weiter?
            left = True
            # Geht's rechts noch weiter?
            right = True
            while True:
                if right:
                    try:
                        b = next(pos)
                    except StopIteration:
                        right = False
                    else:
                        if entry + b <= last:
                            if entry + b + a >= first:
                                snip = ' '.join(
                                        tokens[entry+b+a:entry+b]
                                        ).casefold()
                                if snip in self.tgt_connectors:
                                    return snip
                        else:
                            right = False
                elif not left:
                    break
                if left:
                    try:
                        b = next(non_pos)
                    except StopIteration:
                        left = False
                    else:
                        if entry + b + a >= first:
                            if entry + b <= last:
                                snip = ' '.join(
                                        tokens[entry+b+a:entry+b]
                                        ).casefold()
                                if snip in self.tgt_connectors:
                                    return snip
                        else:
                            left = False
                elif not right:
                    break
        return ''


def main():
    """Starts alignment."""
    logging.basicConfig(filename="results/list/no_matches.log",
                        level=logging.INFO)

    obj1 = ListAligner(
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
    # Alignment with multi-word target connectors.
    europarl_result = obj1.align('de-en/europarl-v7.de-en.de',
                                 'de-en/europarl-v7.de-en.en')
    # Save results df to csv.
    europarl_df = ListAligner.result_to_df(
            europarl_result, save='results/list/list_33_minus16.csv'
            )
    # Save top 10 equivalents for every connector.
    obj1.print_top_values(europarl_df, save='results/list/list_33_minus16.txt')

#    # ===========================================================
#    # Alignment with one-word target connectors.
#    europarl_result = obj1.align('de-en/europarl-v7.de-en.de',
#                                 'de-en/europarl-v7.de-en.en',
#                                 max_window=1)
#    # Save results.
#    europarl_df = ListAligner.result_to_df(
#            europarl_result, save='results/list_approach_oneword.csv'
#            )
#    obj1.print_top_values(europarl_df,
#                          save='results/list_approach_oneword.txt')


if __name__ == "__main__":
    main()
