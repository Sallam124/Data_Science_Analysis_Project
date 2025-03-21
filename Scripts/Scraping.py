import pandas as pd
import os

# Paths clearly defined
wiki_path = r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Games_Season_wiki_Cleaned.csv"
steam_path = r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Game_Seasons(Steam).csv"
output_path = r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Merged_Game_Seasons.csv"

# Load datasets
wiki_df = pd.read_csv(wiki_path)
steam_df = pd.read_csv(steam_path)

# Clearly select columns from wiki dataset (including Release_Season if it exists)
wiki_columns = ['Name', 'Platform', 'Global_Sales', 'EU_Sales', 'NA_Sales', 'Publisher', 'Original_Index']
if 'Release_Season' in wiki_df.columns:
    wiki_columns.append('Release_Season')  # Use the correct column name

wiki_df_selected = wiki_df[wiki_columns]

# Clearly select columns from steam dataset (including Release_Season)
steam_columns = ['Name', 'Position', 'Steam_App_ID']
if 'Release_Season' in steam_df.columns:
    steam_columns.append('Release_Season')

steam_df_selected = steam_df[steam_columns].rename(
    columns={'Position': 'Original_Index', 'Name': 'Steam_Name'}
)

# Merge datasets based on 'Original_Index'
merged_df = pd.merge(wiki_df_selected, steam_df_selected, on='Original_Index', how='outer')

# Prioritize Wiki Name, fill missing with Steam Name
merged_df['Name'] = merged_df['Name'].combine_first(merged_df['Steam_Name'])

# Ensure Release_Season is taken from the correct dataset
merged_df['Release_Season'] = merged_df.get('Release_Season_x', pd.Series()).combine_first(
    merged_df.get('Release_Season_y', pd.Series())
)

# Drop unnecessary duplicated columns if they exist
merged_df.drop(columns=[col for col in ['Release_Season_x', 'Release_Season_y'] if col in merged_df.columns], inplace=True)

# Specify sales unit explicitly (in millions)
merged_df.rename(columns={
    'Global_Sales': 'Global_Sales_Millions',
    'EU_Sales': 'EU_Sales_Millions',
    'NA_Sales': 'NA_Sales_Millions'
}, inplace=True)

# Reorder columns explicitly including Release_Season
final_columns_order = [
    'Name', 'Platform', 'Global_Sales_Millions', 'EU_Sales_Millions', 'NA_Sales_Millions',
    'Publisher', 'Release_Season', 'Original_Index', 'Steam_App_ID'
]
merged_df = merged_df[final_columns_order]

# Save merged dataset explicitly
os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged_df.to_csv(output_path, index=False)

print("Merged dataset saved clearly to:", output_path)
