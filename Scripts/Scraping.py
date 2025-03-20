import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of games clearly defined with App IDs
games = {
    "Counter-Strike: Global Offensive": 730,
    "Dota 2": 570,
    "PUBG: Battlegrounds": 578080,
    "Apex Legends": 1172470
}

# Function clearly defined to scrape active players
def scrape_active_players(app_id):
    url = f'https://steamcharts.com/app/{app_id}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        player_count_div = soup.find("div", class_="app-stat")
        if player_count_div:
            player_count_span = player_count_div.find("span", class_="num")
            if player_count_span:
                return player_count_span.text.strip().replace(",", "")
    return None

# Dictionary clearly defined to store results
results = []

# Loop through each game clearly
for game, app_id in games.items():
    print(f"Scraping data for {game} (App ID: {app_id})...")
    player_count = scrape_active_players(app_id)
    if player_count:
        print(f"{game}: {player_count} active players")
        results.append({"Game": game, "App_ID": app_id, "Active_Players": int(player_count)})
    else:
        print(f"Failed to retrieve data for {game}")

# Convert results clearly to DataFrame
df = pd.DataFrame(results)

# Save clearly to CSV (optional but recommended)
df.to_csv('active_players.csv', index=False)

print("\nScraping completed! Here's the data collected clearly:")
print(df)
