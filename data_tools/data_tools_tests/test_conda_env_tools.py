'''
Description: Tests for conda env tools.py
Dependencies: Requires installation of command line anaconda distribution
How To Use: 
Contributors: rxu17
'''

import os
import sys
import pytest
import unittest
import pandas as pd
from unittest.mock import patch
import wids_datathon_patient_survival.data_tools.conda_env_tools as cet
#from . import conda_env_tools as cet


class TestGetCondaFunctionsValid(unittest.TestCase):
    def setUp(self):
        '''
        '''
        self.env = "test_env" # dummy env

    def test_current_env_path_validity(self):
        ''' Test that current env path is a valid directory
        '''
        dir = os.path.dirname(cet.get_current_env_path())
        self.assertTrue(os.path.exists(dir), "Current env path is invalid!")


    def test_get_env_path_validity(self):
        ''' Test that the selected env is valid
        '''
        self.assertTrue(os.path.exists(cet.get_env_path(self.env)), 
                    "Selected env {} path doesn't exist".format(self.env))

    def test_get_envs_length(self):
        ''' Test that the returned list of env is not empty
        '''
        self.assertTrue(len(cet.get_envs().keys()) > 0,
                   "Envs list is empty!")


    def test_get_envs_validity(self):
        ''' Test that the returned list of env paths are all valid
        '''
        env_paths = cet.get_envs().values()
        self.assertTrue(all([os.path.exists(env_path) 
                    for env_path in env_paths]),
                   "Invalid env_paths found: {}".format(
                       "\n".join([env_path 
                                 for env_path in env_paths 
                                 if not os.path.exists(env_path)]
                                 )))


    def test_package_options(self):
        ''' Test that the list of package options is not empty
        '''
        self.assertTrue(len(cet.package_options().keys()) > 0,
                   "Envs list is empty!")


class TestUserInputFunctions(unittest.TestCase):

    def setUp(self):
        ''' Setup initial dummy variables for testing 
            user input functions
        '''

        self.options = {"1" : "yes",
                        "2" : "no"}
        self.message = "testing?"

    @patch('cet.validate_user_input_exit', return_value='q')
    def test_validate_user_input_exit(self):
        ''' Test that entering q will exit the prompt and script
        '''
        self.assertRaises(cet.validate_user_input_exit(self.options, self.message), 
                          SystemExit, 
                          "validate user input didn't exit when user entered 'q'")

    @patch('cet.validate_user_input_exit', return_value='1')
    def test_validate_user_input_continue(self):
        ''' Testing that a valid user input entered will throw no error
        '''
    try: 
        cet.validate_user_input_exit(self.options, self.message)
    except:
        print("Testing valid user input raised an exception!")


    @patch('cet.validate_user_input_exit', return_value='3')
    def test_validate_user_input_incorrect(self):
        ''' Testing that a invalid user input entered will continue the call
        '''
    try: 
        cet.validate_user_input_exit(self.options, self.message)
    except:
        print("Invalid user input broke the code!")


    @patch('cet.options_select', return_value='1')
    def test_validate_options_select_continue(self):
        ''' Testing that a valid user input entered to an options list for main conda tools
            will throw no error
        '''
    try: 
        cet.options_select()
    except:
        print("Testing valid user input raised an exception!")

    
if __name__ == '__main__':
    unittest.main()