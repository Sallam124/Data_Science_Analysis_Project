import pandas as pd

def clean_steam_data(input_file, output_file):

    df = pd.read_csv(input_file)

    df['Position'] = df.index + 1  


    df_cleaned = df.dropna(subset=['Steam_App_ID'])


    df_cleaned = df_cleaned[['Name', 'Steam_App_ID', 'Position']]

    # Save cleaned data
    df_cleaned.to_csv(output_file, index=False)

    print(f"Cleaned file saved as {output_file}")

input_path = r'Data\Processed\SteamIDs.csv'
output_path = r'Data\Processed\SteamIDs_cleaned2.csv'
clean_steam_data(input_path, output_path)
