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
import pandas as pd
import numpy as np
import db_tools as dbt

def clean_data(filepath):
    df = pd.read_csv(filepath)

def validate_fields():
    pass

def upload_data():
    pass

def main(filepath):
    cleaned = clean_data(filepath)
    validated = validate_fields(cleaned)
    upload_data(validated)

if __name__ == "__main__":
    filepath = sys.argv[1]
    filepath = sys.argv[1]
    main(filepath)