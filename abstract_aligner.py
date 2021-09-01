# -*- coding: utf-8 -*-

"""This module contains a template for all Aligner classes."""

from abc import ABC, abstractmethod

import pandas as pd
import numpy as np


class Aligner(ABC):
    """Template for all Aligner classes."""
    @abstractmethod
    def align(self):
        pass

    @staticmethod
    def note_match(dic, connector, equivalent):
        """Enters new found matches to a dictionary.

        Args:
            dic(dict): Dict to which the connector and equivalent
                        are added in-place.
            connector(str): Source connector.
            equivalent(str): Found target connector.

        """
        if connector not in dic:
            dic[connector] = {equivalent: 1}
            # connector hasn't been aligned to equivalent yet.
        elif equivalent not in dic[connector]:
            dic[connector][equivalent] = 1
            # connector has been aligned to equivalent
            # before.
        else:
            dic[connector][equivalent] += 1

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

    @staticmethod
    def print_top_values(df, save='', top=10):
        """Informs about the highest values of every column.

        Args:
            df(pandas.Dataframe): A Pandas Dataframe.
            save(str): Path to txt-file for extracted information. If empty,
                       information is printed to console.
            top(int): How many values are printed.

        """
        if save:
            out = open(save, 'w', encoding='utf-8')
        else:
            out = None
        print(f'Top {top} of every connector:', end='\n\n', file=out)
        for col in df:
            print(df[col].sort_values(ascending=False).head(top),
                  end='\n\n', file=out)
        if save:
            out.close()
