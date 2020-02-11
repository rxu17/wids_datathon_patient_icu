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
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import seaborn as sb

# possible methods

def one_hot_encoding(input_df):
    ''' This function converts each category value into a new column and 
        assigns a 1 or 0 (True/False) value to the column. 
    '''
    cat_cols = input_df.select_dtypes(include=['object']).columns
    encoded_df = pd.get_dummies(input_df, columns=cat_cols)
    return(encoded_df)


def label_encoding(input_df, priority_cols):
    ''' Encodes the column into numbers (useful for ordinal columns)
    '''
    def encode_column(col):
        input_df[col] = input_df[col].astype('category')
        input_df[col] = input_df[col].cat.codes

    encoded_df = encode_column.apply(lambda x: priority_cols, axis = 1)
    return(encoded_df)


def main():
    input_df = pd.read_csv("/Users/rxu17/Downloads/training_v2.csv")
    encoded_df = one_hot_encoding(input_df)
    encoded_df.to_csv("/Users/rxu17/Downloads/encoded_train.csv")

if __name__ == "__main__":
    main()