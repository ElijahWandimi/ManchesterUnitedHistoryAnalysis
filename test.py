import pandas as pd
import os
from dashboard.data_utils import scrape_data, read_static_data

def test_scrape_data():
    """ Test that the scrape_data function returns a dataframe scraped from the web """
    assert scrape_data().columns.tolist() == read_static_data().columns.tolist()

def test_read_static_data():
    """ Test that the read_static_data function returns a dataframe """
    data_path = os.getcwd() + '/data/matches.csv'
    test_df = pd.read_csv(data_path)
    assert read_static_data().columns.tolist() == test_df.columns.tolist() and read_static_data().shape == test_df.shape

if __name__ == "__main__":
    test_scrape_data()
    test_read_static_data()