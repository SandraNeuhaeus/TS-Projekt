# Python: 3.7.6
# Kodierung: utf-8
"""

"""
from disambiguator import Disambiguator
from list_aligner import ListAligner
import logging


class DisambigAligner(ListAligner):
    """ """

    def __init__(self, src_connectors, tgt_connectors):
        super().__init__('list', src_connectors, tgt_connectors)
        del self.mode


def main():
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


if __name__ == "__main__":
    main()