import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys

# Ensure UTF-8 encoding for console output
sys.stdout.reconfigure(encoding='utf-8')

input_path = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Raw\Kaggle_dataset2(with_ratings).csv'
data = pd.read_csv(input_path)

data['Original_Index'] = data.index

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

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
                        return parsed_date if not pd.isna(parsed_date) else None
        return None
    except Exception as e:
        print(f"Error fetching data for {game_name}: {e}")
        return None

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

print("Starting Wikipedia data fetching...")
data['Wikipedia_Release_Date'] = data['Name'].apply(fetch_wikipedia_release_date)
data['Wikipedia_Release_Season'] = data['Wikipedia_Release_Date'].apply(get_season)

filtered_data = data.dropna(subset=['Wikipedia_Release_Date'])

filtered_output_path = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Games_Season_wiki.csv'
os.makedirs(os.path.dirname(filtered_output_path), exist_ok=True)
filtered_data.to_csv(filtered_output_path, index=False, encoding='utf-8')
print("Filtered data saved at:", filtered_output_path)

df_filtered = pd.read_csv(filtered_output_path)
print(f"Loaded filtered dataset with {len(df_filtered)} rows")

columns_to_drop = ['JP_Sales', 'Other_Sales', 'Critic_Score', 'Critic_Count', 'User_Score', 'Rating', 'Wikipedia_Release_Date']

df_cleaned = df_filtered.drop(columns=columns_to_drop)

cleaned_output_path = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Games_Season_wiki_Cleaned.csv'
os.makedirs(os.path.dirname(cleaned_output_path), exist_ok=True)
df_cleaned.to_csv(cleaned_output_path, index=False)
print(f"Cleaned dataset saved explicitly as: {cleaned_output_path}")