# -*- coding: utf-8 -*-
"""
Python: 3.8.10
Windows 10
"""

import io
import logging
import pandas as pd
import regex as re


class Disambiguator():
    """Does stuff."""

    def __init__(self, alignments_df,
                 patterns=[r", %s", r"%s,"], mode="pattern"):
        self.alignments_df = alignments_df
        self.patterns = patterns
        self.mode = mode

    def disambiguate(self, tgt_path, candidate_list, c_filter=10, p_filter=2):
        """Return a drop_list containing all indices/candidates.

        Args:
            tgt_path(str): directory of the target file, where the
                           candidates have been found by the aligner.
            candidate_list(list): a list containing all candidates/indices
                                  of the alignments_dataframe
            c_filter(int): int that governs, how often a candidate
                           must have been found in one of the self.patterns
                           to be considered a connector.
            d_filter(int): int that governs, how often a candidate must
                           have been found in a punisch_pattern before
                           being put on the drop_list.

        Returns:
            list of strings: drop_list containing all indices/candidates that
                             are to be dropped from alignments_dataframe.
        """
        if self.mode == 'pattern':
            return self.__pattern_disamb(tgt_path, candidate_list, c_filter,
                                         p_filter)

    def __pattern_disamb(self, tgt_path, candidate_list, c_filter, p_filter):
        drop_list = []
        try:
            with io.open(tgt_path, mode="r", encoding="utf-8") as txt_file:
                for candidate in candidate_list:
                    if self.__check_context(candidate, txt_file, c_filter):
                        continue
                    else:
                        drop_list.append(candidate)
                txt_file.seek(0)
                for candidate in candidate_list:
                    if (self.__punish_patterns([r"[a-zA-Z] %s "], candidate,
                                               txt_file, p_filter)):
                        drop_list.append(candidate)
            return drop_list
        except IOError:
            logging.basicConfig(level=logging.ERROR)
            logging.error("ERROR: Could not find the given file")

    def create_candidate_list(self):
        """Create and return the candidate_list for further use.

        Returns:
            list of strings: containing all indices of the self.alignments_df
        """
        return list(self.alignments_df.index)

    def __check_context(self, candidate, txt_file, filter):
        count = 0
        for pattern in self.patterns:
            for line in txt_file:
                stripped_line = line.strip()
                if re.search(pattern % str(candidate), stripped_line,
                             re.IGNORECASE):
                    count += 1
                    if count == filter:
                        return True
        return False

    def __punish_patterns(self, patterns, candidate, txt, p_filter):
        count = 0
        for pattern in patterns:
            for line in txt:
                stripped_line = line.strip()
                if re.search(pattern % str(candidate), stripped_line):
                    count += 1
                    if count == filter:
                        return True
        return False

    def drop_rows(self, drop_list):
        """Return alignment_df after drop_list indixes have beeen removed.

        Args:
            drop_list(list of strings): indices/candidates that are to be
                                        dropped from alignments_dataframe.

        Returns:
            pandas dataFrame: alignments_dataframe after drop_list indixes
                              have beeen removed.
        """
        return self.alignments_df.drop(drop_list)

    @staticmethod
    def create_non_con_dict(connector_list, tgt_path):
        """Show which of the non-connector occurences for every connector.

        Args:
            connector_list(list of strings):
                connectors for which the non-connector occurences
                are to be found.
            tgt_path(str): directory of the file containing the connectors.

        Returns:
            tuple: containing two dictionaries. The first dictionary
                   has the structure connector: [non_connector occurences]
                   The second one contains how many occurrences there were
                   overall for every connector.
        """
        not_connectors = {}
        con_total_occs = {}
        try:
            with io.open(tgt_path, mode="r", encoding="utf-8") as txt_file:
                for connector in connector_list:
                    connector_occs = []
                    not_connectors[connector] = []
                    txt_file.seek(0)
                    for line in txt_file:
                        stripped_line = line.strip()
                        if re.search(r". %s ." % connector, stripped_line,
                                     re.IGNORECASE):
                            connector_occs.append(re.findall(
                                r". %s ." % connector, stripped_line,
                                re.IGNORECASE)[0])
                    con_total_occs[connector] = len(connector_occs)
                    for i in range(0, len(connector_occs)):
                        if re.search(r"[a-zA-Zß0-9\(\)\'\"öüä ] %s [a-zA-Z0-9\(öüäÄÜÖ\)]"
                                     % connector, connector_occs[i]):
                            not_connectors[connector].append(i)
            return (not_connectors, con_total_occs)
        except IOError:
            logging.basicConfig(level=logging.ERROR)
            logging.error("ERROR: Could not find the given file")


def main():
    """Drop non-connector rows from alignments_df."""
    logging.basicConfig(level=logging.DEBUG)
    disa = Disambiguator(pd.read_csv("naive.csv"))
    logging.debug("Finished loading")
    can_list = disa.create_candidate_list()
    dropped = disa.drop_rows(disa.disambiguate('europarl-v7.de-en.en',
                                               can_list, 21))
    dropped_sorted = dropped.sort_values("andererseits", "index",
                                         ascending=False)
    logging.debug("Finished disamb")
    dropped.to_csv('dropped.csv')
    # print(dropped_sorted)
    # logging.debug(str(dropped_sorted.shape))
    """Create non_connector_dictionary."""
    non_con = Disambiguator.create_non_con_dict(['aber', 'doch', 'jedoch',
                                                 'allerdings', 'andererseits',
                                                 'hingegen'],
                                                r"europarl-v7.de-en.de")
    print(non_con[0])


if __name__ == "__main__":
    main()
