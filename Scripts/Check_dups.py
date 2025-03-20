import pandas as pd

def clean_steam_data(input_file, output_file):
    # Load dataset
    df = pd.read_csv(input_file)

    # Add Position column before filtering
    df['Position'] = df.index + 1  # Making position 1-based

    # Keep only rows with a valid Steam_App_ID
    df_cleaned = df.dropna(subset=['Steam_App_ID'])

    # Select only necessary columns
    df_cleaned = df_cleaned[['Name', 'Steam_App_ID', 'Position']]

    # Save cleaned data
    df_cleaned.to_csv(output_file, index=False)

    print(f"Cleaned file saved as {output_file}")

# Example usage
input_path = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\SteamIDs.csv'
output_path = r'Data\Processed\SteamIDs_cleaned2.csv'
clean_steam_data(input_path, output_path)
