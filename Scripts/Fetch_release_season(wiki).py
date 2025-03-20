import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

# Load your dataset
input_path = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Raw\Kaggle_dataset2(with_ratings).csv'
data = pd.read_csv(input_path)

# Define headers to avoid Wikipedia blocking requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

# Function to fetch release date from Wikipedia
def fetch_wikipedia_release_date(game_name):
    try:
        url = f'https://en.wikipedia.org/wiki/{game_name.replace(" ", "_")}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            infobox = soup.find('table', class_='infobox')
            
            if infobox:
                rows = infobox.find_all('tr')
                for row in rows:
                    header = row.find('th')
                    if header and ('Release' in header.text or 'release' in header.text):
                        date = row.find('td').text.strip().split('\n')[0]
                        parsed_date = pd.to_datetime(date, errors='coerce')
                        return parsed_date
        return None
    except:
        return None

# Function to determine the season from the release date
def get_season(date):
    if pd.isnull(date):
        return None
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

# Adding new columns explicitly
data['Wikipedia_Release_Date'] = None
data['Wikipedia_Release_Season'] = None

# Loop through each game title to fetch Wikipedia release dates
for idx, row in data.iterrows():
    game_title = row['Name']
    print(f"Fetching Wikipedia data for {game_title}...")
    release_date = fetch_wikipedia_release_date(game_title)
    season = get_season(release_date)

    data.at[idx, 'Wikipedia_Release_Date'] = release_date
    data.at[idx, 'Wikipedia_Release_Season'] = season

    print(f"{game_title} | Release Date: {release_date} | Season: {season}")

# Ensure processed directory exists
output_path = 'Data\Processed\games_with_releasedates(byseason).csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save your enhanced dataset
data.to_csv(output_path, index=False)

print("\nWikipedia scraping completed. Data saved clearly:", output_path)
