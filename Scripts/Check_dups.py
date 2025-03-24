import pandas as pd

# Load the dataset
file_path = r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Final\Merged_Final.csv"
df = pd.read_csv(file_path)

# Print missing values per column
print("Missing values before imputation:")
print(df.isnull().sum())

# # For numeric columns, fill with the median
# numeric_columns = ['User_Score', 'Price', 'Year_of_Release']
# for col in numeric_columns:
#     median_val = df[col].median()
#     df[col] = df[col].fillna(median_val)

# # For categorical columns, fill with the mode (most frequent value)
# categorical_columns = ['Release_Season', 'Developer', 'Rating', 'Publisher']
# for col in categorical_columns:
#     mode_val = df[col].mode()[0]  # Using the first mode
#     df[col] = df[col].fillna(mode_val)

# For Steam_App_ID, fill missing with a placeholder (if appropriate)

df['Steam_App_ID'] = df['Steam_App_ID'].fillna(-1)

print("\nMissing values after imputation:")
print(df.isnull().sum())

# Save the updated dataset
output_file = r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Final\Merged_Final_Filled.csv"
df.to_csv(output_file, index=False)
