#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 15:44:16 2021

@author: sandra
"""

import random
import pandas as pd
import logging

from tqdm import tqdm

from align_connectors import Aligner
from split_text import token_split

logging.basicConfig(filename="info.log",
                    level=logging.WARNING)

class ListAligner(Aligner):
    def __init__(self, mode, src_connectors, tgt_connectors):
        super().__init__(src_connectors, mode)
        self.src_connectors = self.connectors
        self.tgt_connectors = tgt_connectors
        self.alignments = dict()
        del self.connectors

    def align(self, src_path, tgt_path):
        super().align(src_path, tgt_path)
        if self.mode == 'list':
            return self.__list_align(src_path, tgt_path)

    def __list_align(self, src_path, tgt_path):
        with open(src_path, encoding='utf-8') as src_file, \
             open(tgt_path, encoding='utf-8') as tgt_file:
            lineno = 1
            pbar = tqdm(total=1920209)
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
                    equivalent = ''
                    if not tgt_tokens:
                        break
                    if token in self.src_connectors:
                        # Set maxdist <- distance to sentence edge
                        if len(tgt_tokens)-1-token_id >= token_id:
                            # Distance to left sentence edge is smaller.
                            maxdist = token_id
                        else:  # Distance to right sentence edge is smaller.
                            maxdist = len(tgt_tokens)-1-token_id
                        # Search target connector.
                        dist = 0
                        for dist in range(maxdist+1):
                            # Look at left and right of token.
                            if (tgt_tokens[token_id-dist]
                                    in self.tgt_connectors):
                                if (tgt_tokens[token_id+dist]
                                        in self.tgt_connectors):
                                    # Two tokens with same dist are connectors.
                                    # This case is not very likely.
                                    equivalent = random.choice(
                                            [tgt_tokens[token_id-dist],
                                             tgt_tokens[token_id+dist]]
                                            )
                                    break
                                else:
                                    equivalent = tgt_tokens[token_id-dist]
                                    break
                            else:
                                if (tgt_tokens[token_id+dist]
                                        in self.tgt_connectors):
                                    equivalent = tgt_tokens[token_id+dist]
                                    break
                            dist += 1
                        # If token_id > len(tgt_tokens)-1, set
                        # dist so that searching starts at end of tgt_tokens.
                        if maxdist < 0:
                            dist = token_id - (len(tgt_tokens)-1)
                        if token_id - dist > 0:
                            # Search equivalents at left.
                            for index in range(token_id-dist, 0, -1):
                                if tgt_tokens[index] in self.tgt_connectors:
                                    equivalent = tgt_tokens[index]
                                    break
                        elif token_id + dist < len(tgt_tokens):
                            # Search equivalents at right.
                            for index in range(token_id+dist, len(tgt_tokens)):
                                if tgt_tokens[index] in self.tgt_connectors:
                                    equivalent = tgt_tokens[index]
                                    break
                        # Add equivalent to alignments.
                        self.note_match(token, equivalent)
                        if not equivalent:
                            logging.info(f'No match: Line {lineno} ({token})')
                    token_id += 1
                lineno += 1
                pbar.update(1)
            pbar.close()
        return self.alignments

    def note_match(self, connector, equivalent):
        """ """
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
    obj1 = ListAligner(
            mode='list',
            src_connectors = {'aber', 'doch', 'jedoch',
                              'allerdings', 'andererseits', 'hingegen'},
            tgt_connectors = {'but', 'however', 'though',
                              'although', 'yet', 'nevertheless',
                              'nonetheless', 'albeit', 'otherwise',
                              'whereas', 'again'}
            )
    europarl_result = obj1.align('de-en/europarl-v7.de-en.de',
                                 'de-en/europarl-v7.de-en.en')
    print(ListAligner.result_to_df(europarl_result, save='list_approach.csv'))

    europarl_df = pd.read_csv('list_approach.csv', index_col=0)
    for col in europarl_df:
        print(europarl_df.sort_values(by=col, ascending=False).head(10))


if __name__ == "__main__":
    main()
