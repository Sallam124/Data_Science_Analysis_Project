import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_season(date_str):
    """Converts date string to season."""
    if not date_str or date_str == "NaT":
        return None

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        month = date.month
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        elif month in [9, 10, 11]:
            return "Fall"
    except ValueError:
        return None

def fetch_release_date(app_id):
    """Fetch exact release date from Steam store page."""
    if pd.isna(app_id):
        return None
    
    url = f'https://store.steampowered.com/app/{int(app_id)}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        date_div = soup.find('div', class_='date')
        if date_div:
            date_str = date_div.text.strip()
            for fmt in ("%d %b, %Y", "%b %d, %Y", "%d %B %Y", "%B %d, %Y"):
                try:
                    parsed_date = datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                    return parsed_date
                except ValueError:
                    continue
    return None

def process_steam_data(input_file, output_file):
    df = pd.read_csv(input_file)
    print(f"Loaded dataset with {len(df)} rows")

    if 'Steam_App_ID' not in df.columns:
        print("Error: 'Steam_App_ID' column not found.")
        return

    df["Release_Date"] = df["Steam_App_ID"].apply(fetch_release_date)
    df["Season"] = df["Release_Date"].apply(get_season)

    df.to_csv(output_file, index=False)
    print(f"Processed file saved as {output_file}")

# Paths explicitly defined
input_path = r"Data\Processed\SteamIDs_Cleaned.csv"
output_path = r"Data\Processed\Game_Seasons(Steam).csv"
process_steam_data(input_path, output_path)
