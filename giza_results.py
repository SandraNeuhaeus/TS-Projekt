# -*- coding: utf-8 -*-

"""
"""

import re

from split_text import token_split

RESULTSFILE = 'giza-pp/europarl_data/output/Result.A3.final'
#RESULTSFILE = 'giza-pp/europarl_data/input/Source_Target.cooc'
SRC_CONNECTORS = {'aber',
              'doch',
              'jedoch',
              'allerdings',
              'andererseits',
              'hingegen'
              }

with open(RESULTSFILE, encoding='utf-8') as results:
#    n = 0
#    while n < 10:
#        print(next(results))
#        n += 1
#    while True:
#        try:
#            line = next(results)
#        except StopIteration:
#            print(line)
#            break
    alignments = dict()
    for line in results:
        if line.startswith('#'):
#            match = re.search(r'source length ([0-9]+)', line)
#            if match:
#                src_len = match.group(1)
#            match = re.search(r'target length ([0-9]+)', line)
#            if match:
#                tgt_len = match.group(1)
#            if src_len > tgt_len:
#                alignments00 += 1
        elif line.startswith('NULL'):
            tokens = line.split(' ')
            i = 0
            while i < len(tokens):
                if tokens[i] in SRC_CONNECTORS:
                    i += 2
                    equivalent_toks = []
                    while tokens[i].isnumeric():
                        equivalent_toks.append(english_toks[tokens[i]])
                        i += 1
                    equivalent = ' '.join(equivalent_toks)
                i += 1
        else:
            english_toks = line.split(' ')



        else:
            pass

