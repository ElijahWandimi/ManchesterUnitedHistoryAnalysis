import numpy as np
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import time

# Create a function to scrape the data and chache it
def scrape_data():
    all_matches = []
    years = list(range(2023, 2019, -1))


    for year in years:
        url = 'https://fbref.com/en/squads/19538871/Manchester-United-Stats'
        dt = requests.get(url)
        soup = BeautifulSoup(dt.text, 'html.parser')

        prev_season = f'{year-2}-{year-1}'
        url = f"https://fbref.com{prev_season}"

        matches = pd.read_html(dt.text, match="Scores & Fixtures ")[0]
    
        shooting_link = list(set([f"https://fbref.com{l}" for l in [link.get('href') for link in soup.find_all('a')] if l and 'all_comps/shooting/' in l]))
        shooting_data = requests.get(shooting_link[0])
        shooting_df = pd.read_html(shooting_data.text, match='Shooting')[0]
        shooting_df.columns = shooting_df.columns.droplevel(0)

        try:
            team_df = matches.merge(shooting_df[['Date','Dist', 'Sh', 'SoT', 'FK', 'PK', 'PKatt']], on='Date', how='left')
        except ValueError:
            print(f'No shooting data for {year}')
            continue

        team_df = team_df[team_df['Comp'] == 'Premier League']
        team_df['Season'] = year

        all_matches.append(team_df) 
        time.sleep(1)

    return pd.concat(all_matches)

def read_static_data():
    data_path = os.getcwd() + '/data/matches.csv'
    return pd.read_csv(data_path)

if __name__ == "__main__":
    read_static_data()
    scrape_data()

