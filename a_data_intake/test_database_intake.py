import os
import unittest
from wids_datathon_patient_survival.a_data_intake import database_intake as di

class TestUtils(unittest.TestCase):

    def setUp(self):
        '''
        '''
        self.filepath = "/Users/rexxx/Documents/Projects/widsdatathon2020/training_v2.csv"


    def test_clean_data(self):
        '''
        '''
        df = di.clean_data(self.filepath)
        for subset in df:
            self.assertTrue(len(subset) > 0, "Dataset has no rows!")
            self.assertFalse(all(subset), "Dataset has no rows!")


    def tearDown(self):
        '''
        '''
        

if __name__ == "__main__":
    unittest.main()
