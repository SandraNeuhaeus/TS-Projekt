#      Python: 3.7.6
#   Kodierung: utf-8
""" """
from nltk.tokenize import word_tokenize
from tqdm import tqdm


class Aligner():
    """ """

    def __init__(self, connectors, mode='naive'):
        self.connectors = connectors
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
        """ """
        alignments = dict()
        src_file = open(src_path, encoding='utf-8')
        tgt_file = open(tgt_path, encoding='utf-8')
        tgt_text = [word_tokenize(l.casefold()) for l in tqdm(tgt_file.readlines())]
        tgt_file.close()
        line_id = 0
        for line in tqdm(src_file.readlines()):
            tokens = word_tokenize(line.casefold())
            token_id = 0
            for token in tokens:
                actual_token_id = token_id
                if token in self.connectors:
                    if (token_id >= len(tgt_text[line_id])
                        and len(tgt_text[line_id]) > 0):
                        token_id = len(tgt_text[line_id]) - 1
                        if tgt_text[line_id][token_id] in ['.', ',',
                                                           '!', '?']:
                            token_id -= 1
                    equivalent = tgt_text[line_id][token_id]
                    if token not in alignments:
                        alignments[token] = {equivalent: 1}
                    elif equivalent not in alignments[token]:
                        alignments[token][equivalent] = 1
                    else:
                        alignments[token][equivalent] += 1
                if actual_token_id != token_id:
                    break
                token_id += 1
            line_id += 1
        src_file.close()
        return alignments


def main():
    obj1 = Aligner({'aber', 'doch', 'jedoch',
                    'allerdings', 'andererseits', 'hingegen'})
    print(obj1.align('test.de', 'test.en'))
    print(obj1.align('de-en/europarl-v7.de-en.de', 'de-en/europarl-v7.de-en.en'))


if __name__ == "__main__":
    main()
