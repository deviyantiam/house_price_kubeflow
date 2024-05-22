import os
import unittest
import pandas as pd
import pickle
from app import HousePriceModel
from dotenv import load_dotenv
from unittest.mock import patch

load_dotenv()

class TestHousePriceModel(unittest.TestCase):
    def setUp(self):
        self.predict_price = HousePriceModel("test_model")
        self.model_path = os.getenv("MODEL")
        self.train_path = os.getenv("TRAIN_DF")
        with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)

    def test_load(self):
        with patch('app.HousePriceModel.load') as mock_load:
            self.predict_price.load(self.model_path)
            mock_load.assert_called_once_with(self.model_path)

    def test_convert_columns_to_binary(self):
        # Test case when column is 'yes'
        test_df = {'col1': ['yes']}
        df = self.predict_price.convert_columns_to_binary(pd.DataFrame(test_df), ['col1'])
        self.assertEqual(df['col1'][0], 1)

        # Test case when column is not 'yes'
        test_df = {'col1': ['no']}
        df = self.predict_price.convert_columns_to_binary(pd.DataFrame(test_df), ['col1'])
        self.assertEqual(df['col1'][0], 0)

    def test_convert_furnish_column(self):
        # Test case for test
        test_df = {'furnishingstatus': ['furnished']}
        df = self.predict_price.convert_furnish_column(pd.DataFrame(test_df), 'test', ['furnishingstatus'])
        self.assertTrue('furnishingstatus_furnished' in df.columns)

    
    def test_predict_one(self):
        # Mocking request data
        request = {
            "area": 1000,
            "bedrooms": 2,
            "bathrooms": 2,
            "stories": 2,
            "mainroad": "yes",
            "guestroom": "no",
            "basement": "yes",
            "hotwaterheating": "no",
            "airconditioning": "yes",
            "parking": 1,
            "prefarea": "yes",
            "furnishingstatus": "semi-furnished"
        }
        prediction = self.predict_price.predict_one(request)
        self.assertEqual(prediction['predictions'][0]['prediction'], 4354000)

if __name__ == '__main__':
    unittest.main()