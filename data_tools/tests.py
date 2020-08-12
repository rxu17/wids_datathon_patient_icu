
'''
Description: General tests to use around pipeline
How To Use: 
Contributors: rxu17
'''

import os
import sys

def test_filepath(filepath):
    ''' series of tests for filepath:
        -Check for read access
        -Check for write access
        -Check for execution access'''
    assert(os.path.isdir(filepath), "Dir doesn't exist")
    assert(os.access(filepath, os.R_OK), "Dir not readable") 
    assert(os.access(filepath, os.W_OK), "Dir not writeable")
    assert(os.access(filepath, os.X_OK), "Dir not executable")


def test_file(file):
    ''' series of tests for file, check it exists and is writable/readable'''
    assert(os.path.isfile(), "File:{} doesn't exist".format(file))
    try:
        f = open(file)
    except IOError:
        print("File:{} not accessible".format(file))
    finally:
        f.close()