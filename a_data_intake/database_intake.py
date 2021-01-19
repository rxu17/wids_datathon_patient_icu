# -*- coding: utf-8 -*-
'''
Description: Used to save raw data to database table for
faster retrieval of estimates
Contents:
How To Use:
Contributors: rxu17
'''

import re
import time
import os
import sys
import logging
import pandas as pd
import numpy as np
from wids_datathon_patient_survival.data_tools import db_tools as dbt


def clean_data(filepath : str) -> pd.DataFrame:
    df = pd.read_csv(filepath, chunksize = 1000)
    import pdb; pdb.set_trace()
    return(df)


def validate_fields(df):
    return(df)


def upload_to_db(conn : str, filepath : str):
    for subset in clean_data(filepath):
        print(subset)
        dbt.upload_data(connection = conn,
                        df = subset, 
                        table = "input_data", 
                        action = "update")


def main(filepath: str):
    cleaned = clean_data(filepath)
    validated = validate_fields(cleaned)
    conn = dbt.get_connect_cursor("rex_test.db")
    upload_to_db(conn, filepath)


if __name__ == "__main__":
    filepath = sys.argv[1]
    main(filepath)