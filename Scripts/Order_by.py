import pandas as pd
import os

# Paths
dup_free_path = r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Dup_Free Merged_Games (per season).csv"

# Load datasets
dup_free_df = pd.read_csv(dup_free_path)

# Sorting options (commented out except for Season)
# merged_df.sort_values(by='Name', inplace=True)
# merged_df.sort_values(by='Platform', inplace=True)
# merged_df.sort_values(by='Global_Sales_Millions', inplace=True, ascending=False)
# merged_df.sort_values(by='EU_Sales_Millions', inplace=True, ascending=False)
# merged_df.sort_values(by='NA_Sales_Millions', inplace=True, ascending=False)
# merged_df.sort_values(by='Publisher', inplace=True)
dup_free_df.sort_values(by='Release_Season', inplace=True)  # Active sort

# Save to the same file or new output if desired
dup_free_df.to_csv(dup_free_path, index=False)

print("Merged_Game_Seasons.csv sorted by Release_Season.")
