import requests
import pandas as pd

# Load dataset
data = pd.read_csv(r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Raw\Kaggle_dataset2(with_ratings).csv")

# Fetch Steam games data from SteamSpy
print("Fetching Steam games data...")
response = requests.get("https://steamspy.com/api.php?request=all")
steam_games = response.json()

# Create a mapping of game titles to App IDs
steam_game_ids = {details['name'].lower(): appid for appid, details in steam_games.items()}

# Function to get App ID, handling NaN values
def get_app_id(game_title):
    if isinstance(game_title, str):
        return steam_game_ids.get(game_title.lower())
    return None

# Apply function to get App IDs
data['Steam_App_ID'] = data['Name'].apply(get_app_id)

# Remove rows with missing Steam_App_ID
data_cleaned = data.dropna(subset=['Steam_App_ID'])

# Save only 'Name' and 'Steam_App_ID' to CSV
data_cleaned[['Name', 'Steam_App_ID']].to_csv('Data\Processed\SteamIDs_Cleaned.csv', index=False)

print("Saved cleaned Steam IDs successfully.")
