'''
Description: Tests for conda env tools.py
Dependencies: Requires installation of command line anaconda distribution
How To Use: python test_conda_env_tools.py
Contributors: rxu17
'''

import os
import sys
import time
import pytest
import unittest
import pandas as pd
from unittest.mock import patch
import wids_datathon_patient_survival.data_tools.conda_env_tools as cet


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

    @patch('builtins.input', return_value='q')
    def test_validate_user_input_exit(self, mock_input):
        ''' Test that entering q will exit the prompt and script
        '''
        self.assertRaises(cet.validate_user_input(self.options, self.message), 
                          SystemExit, 
                          "validate user input didn't exit when user entered 'q'")


    @patch('builtins.input', return_value='1')
    def test_validate_user_input_continue(self, mock_input):
        ''' Testing that a valid user input entered will throw no error
            and return a valid key in dummy options 
        '''
        self.assertTrue(cet.validate_user_input(self.options, self.message) in self.options.keys(), 
                            "Testing valid user input raised an exception!")


    @patch('builtins.input', return_value='q')
    def test_validate_user_input_incorrect(self, mock_input):
        ''' Testing that a invalid user input entered will continue the call
        '''
        try: 
            cet.validate_user_input(self.options, self.message)
        except:
            print("Invalid user input broke the code!")


    @patch('builtins.input', return_value='q')
    def test_validate_options_select_continue(self, mock_input):
        ''' Testing that a valid user input entered to an options list for main conda tools
            will throw no error
        '''
        try: 
            cet.options_select()
        except:
            print("Testing valid user input raised an exception!")


class TestEnvFunctions(unittest.TestCase):

    def setUp(self):
        ''' Setup initial dummy variables for testing 
            conda env creation
        '''
        self.env = "test"
        self.option = "a"
        self.save_path = "/Users/rexxx/Documents/Projects/wids_datathon_patient_survival/to_copy.yaml"
        self.os_create_call = "conda env export > {} -n {}".format(self.save_path, self.env)
        self.os_create_file= "conda env create -f {}".format(self.save_path)
        self.os_create_new = "conda create -n {}".format(self.env)


    @patch('os.system')
    @patch('builtins.input', return_value='2')
    @patch('builtins.input', return_value='a')
    @patch('builtins.input', return_value='test_hi')
    def test_create_env_from_file(self, mock_input1, mock_input2, mock_input3, mock_system):
        ''' Testing the creation of env from file
        '''
        cet.create_env()
        mock_system.assert_called_once_with(self.os_create_call)
        mock_system.assert_called_once_with(self.os_create_file)


    @patch('os.system')
    @patch('builtins.input', return_value='b')
    @patch('builtins.input', return_value='test_hi')
    def test_create_env_new(self, mock_input1, mock_input2, mock_input3, mock_system):
        ''' Testing the creation of env from scratch
        '''
        cet.create_env()
        mock_system.assert_called_once_with(self.os_create_new)


if __name__ == '__main__':
    unittest.main()