"""
Unit Tests for the Utils
"""
import unittest
import pandas as pd
from src.utils import verify_number_elements, \
    verify_range_records, verify_positive_values, \
    most_popular_device, weekday

class TestUtils(unittest.TestCase):
    """ Test Class for the Utils """

    def setUp(self):
        """
        Set useful configurations/variables to be used
        """
        data = {'time': ['2020-04-24 00:00:00+00:00', '2020-04-25 00:00:00+00:00',
                         '2020-04-26 00:00:00+00:00', '2020-04-27 00:00:00+00:00'],
                '19': [12, 12, 12, 13],
                '20': [12, 12, 12, 14],
                '21': [12, 12, 12, 15],
                '22': [12, 12, 12, 13],
                '23': [12, 12, 12, 18],
                '24': [12, 12, 12, 20],
                '25': [12, 12, 12, 23],
                '26': [12, 12, 12, 20],
                }
        self.dataframe = pd.DataFrame(data=data)


    def test_verify_number_elements(self):
        """ Test verify_number_elements method """
        count_elements = verify_number_elements(self.dataframe, 2)
        assert count_elements==4

    def test_verify_range_records(self):
        """ Test verify_range_records method """
        count_results = verify_range_records(self.dataframe, '2020-04-24', '2020-04-25')
        assert count_results==2

    def test_verify_positive_values(self):
        """ Test verify_positive_values method """
        number_negatives_values = verify_positive_values(self.dataframe, 4)
        assert number_negatives_values==0

    def test_most_popular_device(self):
        """ Test most_popular_device method """
        popular_device = most_popular_device(self.dataframe)
        assert popular_device == '25'

    def test_weekday(self):
        """ Test weekday method """
        number_day = weekday('2022-08-01 00:00:00+00:00')
        assert number_day == 0


if __name__ == "__main__":
    unittest.main()

