# Unit tests for wu_cleaning.py
import unittest
import numpy as np
import pandas as pd

from wu_cleaning import clean_obs_data

class TestWuCleaning(unittest.TestCase):

    # Test number of columns
    def test_wu_cleaning(self):

        #create a dummy dataframe to test the cleaning
        dummy_data = pd.DataFrame({'TemperatureF': [0,50,150], 'DewpointF': \
        [-99.9, 50, 80], 'PressureIn': [0,30,50], 'WindDirectionDegrees': \
        [-50, 50, 500], 'Humidity': [-50,50,150]})

        clean_data = clean_obs_data(dummy_data)

        self.assertFalse((clean_data.ix[:,0] <= 10).any())
        self.assertFalse((clean_data.ix[:,0] >= 125).any())

        self.assertFalse((clean_data.ix[:,1] == -99.9).any())
        self.assertFalse((clean_data.ix[:,1] >= 80).any())

        self.assertFalse((clean_data.ix[:,2] <= 25).any())
        self.assertFalse((clean_data.ix[:,2] >= 31.5).any())

        self.assertFalse((clean_data.ix[:,3] < 0).any())
        self.assertFalse((clean_data.ix[:,3] >= 360).any())

        self.assertFalse((clean_data.ix[:,4] <= 0).any())
        self.assertFalse((clean_data.ix[:,4] > 100).any())

if __name__ == '__main__':
    unittest.main()