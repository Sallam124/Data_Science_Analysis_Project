import pandas as pd
import os

# Define file paths explicitly
input_file = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Game_Seasons_Steam.csv'
output_file = r'C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Dup_Free_Steam.csv'

# Load the dataset
df = pd.read_csv(input_file)

# حذف التكرار حسب Steam_App_ID فقط، واحتفظ بأول نسخة من كل ID
df_cleaned = df.drop_duplicates(subset='Steam_App_ID', keep='first')

# حفظ الملف الجديد
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df_cleaned.to_csv(output_file, index=False)

print(f" Cleaned dataset with unique Steam_App_IDs saved to: {output_file}")
