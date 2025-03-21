import pandas as pd
import os

# Define file paths explicitly
input_file = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Merged_Game_Seasons.csv'
output_file = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Dup_Free Merged_Games (per season).csv'

# Load dataset clearly
df = pd.read_csv(input_file)

# Separate records with and without Steam_App_ID
has_steam_id = df.dropna(subset=['Steam_App_ID'])
no_steam_id = df[df['Steam_App_ID'].isna()]

# Drop duplicates explicitly based on Steam_App_ID
has_steam_id_cleaned = has_steam_id.drop_duplicates(subset=['Steam_App_ID'], keep='first')

# For records without Steam_App_ID, drop duplicates based explicitly on Name and Platform
no_steam_id_cleaned = no_steam_id.drop_duplicates(subset=['Name', 'Platform'], keep='first')

# Combine cleaned datasets explicitly
df_final = pd.concat([has_steam_id_cleaned, no_steam_id_cleaned], ignore_index=True)

# Save cleaned dataset explicitly
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df_final.to_csv(output_file, index=False)

print(f"Duplicates removed based on Steam_App_ID and Name/Platform combination. Cleaned dataset saved clearly as: {output_file}")
