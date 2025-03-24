import pandas as pd

# File path
Merged_Final = r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Final\Merged_Final.csv"

# Load dataset
merged_df = pd.read_csv(Merged_Final)

# Sorting options (commented out except for Season)
#merged_df.sort_values(by='Name', inplace=True)
#merged_df.sort_values(by='Platform', inplace=True)
merged_df.sort_values(by='Global_Sales_Millions', inplace=True, ascending=False)
#merged_df.sort_values(by='EU_Sales_Millions', inplace=True, ascending=False)
#merged_df.sort_values(by='NA_Sales_Millions', inplace=True, ascending=False)
#merged_df.sort_values(by='Publisher', inplace=True)
# merged_df.sort_values(by='Release_Season', inplace=True)  # Active sort
# Save to the same file
merged_df.to_csv(Merged_Final, index=False)

print("Merged_Final.csv sorted by Global_Sales_Millions.")
