# -*- coding: utf-8 -*-
'''
Description: Used to transform icu health data, such as converting categorical 
data into numeric, or creating new indicators
Contents:
How To Use:
Contributors: rxu17
'''

import re
import time
import os
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import seaborn as sb


def one_hot_encoding(input_df):
    ''' This function converts each category value into a new column and 
        assigns a 1 or 0 (True/False) value to the column.

        Parameters:
            input_df: dataframe with object columns

        Returns: df with all possible val in each object column 
        encoded as a true/false columns
    '''
    cat_cols = input_df.select_dtypes(include=['object']).columns
    assert(len(cat_cols) > 0), "Error: input_df has no object columns"
    encoded_df = pd.get_dummies(input_df, columns=cat_cols)
    return(encoded_df)


def label_encoding(input_df, priority_cols):
    ''' Encodes the column into numbers (useful for ordinal columns)

        Parameters:
            priority_cols: list of cols in df to encode
            input_df: dataframe of our input_df
        
        Returns: df with selected variables encoded
    '''
    assert(set(priority_cols) <= set(input_df.columns)), \
                "Error: columns don't exist in input_df"
    def encode_column(col):
        input_df[col] = input_df[col].astype('category')
        input_df[col] = input_df[col].cat.codes

    encoded_df = encode_column.apply(lambda x: priority_cols, axis = 1)
    return(encoded_df)


def variable_binning(input_df, bin_info):
    ''' For when we want to bin variables into different groups whether for 
        better estimates when we have too many categories or cap creation

        Paramaters:
            input_df: our input df for variable binning
            bin_info: dict of keys being bin cols and values being bin widths

        Returns: df with selected variables binned
    '''
    assert(isinstance(bin_info, 'dict') & set(bin_info.keys()) <= set(input_df.columns)), \
        "Error: bin_info is not a dictionary object and/or columns to bin doesn't exist in input_df"
    for col in bin_info.keys():
        assert(bin_info[col] < max(input_df[col]) - min(input_df[col])) \
            "bin width of {wid} for column {col} is too big".format(wid = bin_info[col], col = col)
        if col == "age":
            bins = np.arange(1, 100, bin_info[col]) 
        else:
            bins = np.arange(math.floor(min(input_df[col])), math.floor(max(input_df[col])), bin_widths[col]) 
        labels = list(range(1, len(bins)))
        input_df['{}_bin'.format(col)] = pd.cut(df[col], bins=bins, labels=labels)
    return(input_df)

def main():
    input_df = pd.read_csv(paste0(getwd(), "/training_v2.csv"))
    encoded_df = one_hot_encoding(input_df)
    encoded_df.to_csv(paste0(getwd(), "/encoded_df.csv"))

if __name__ == "__main__":
    main()