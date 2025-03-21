import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set save directory
save_dir = r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data_Analysis and exploration\Combined"
os.makedirs(save_dir, exist_ok=True)

# Load dataset
df = pd.read_csv(r"C:\Users\salla\OneDrive\Desktop\Data_Science_Project\Data\Processed\Dup_Free Merged_Games .csv")

# Remove non-relevant columns from summary statistics
summary_stats = df.drop(columns=['Steam_App_ID', 'Original_Index']).describe()
summary_stats.to_csv(os.path.join(save_dir, "summary_statistics.csv"))
print("Summary statistics saved to summary_statistics.csv")

# Check for missing values
missing_values = df.isnull().sum()
missing_values.to_csv(os.path.join(save_dir, "missing_values.csv"))
print("Missing values saved to missing_values.csv")

# Check for duplicates
duplicates = df.duplicated().sum()
with open(os.path.join(save_dir, "duplicates.txt"), "w") as f:
    f.write(f"Duplicate Rows: {duplicates}\n")
print("Duplicate count saved to duplicates.txt")

# Identify outliers using IQR
numerical_columns = ['NA_Sales_Millions', 'EU_Sales_Millions', 'Global_Sales_Millions']
outliers = {}
for col in numerical_columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers[col] = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
outlier_counts = {col: outlier_data.shape[0] for col, outlier_data in outliers.items()}
pd.DataFrame.from_dict(outlier_counts, orient='index', columns=['Outlier Count']).to_csv(os.path.join(save_dir, "outliers.csv"))
print("Outlier counts saved to outliers.csv")

# Histograms
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
sns.histplot(df['Global_Sales_Millions'], bins=30, kde=True)
plt.xlabel("Global Sales (Millions)")
plt.ylabel("Game Frequency")
plt.title("Distribution of Global Sales")

plt.subplot(1, 2, 2)
sns.histplot(df['NA_Sales_Millions'], bins=30, kde=True)
plt.xlabel("NA Sales (Millions)")
plt.ylabel("Game Frequency")
plt.title("Distribution of NA Sales")

plt.tight_layout()
plt.savefig(os.path.join(save_dir, "histograms.png"))
print("Histograms saved as histograms.png")
plt.close()

# Box plots for sales distributions
plt.figure(figsize=(10, 5))
sns.boxplot(data=df[['NA_Sales_Millions', 'EU_Sales_Millions', 'Global_Sales_Millions']])
plt.title("Boxplot of Sales Data")
plt.ylabel("Values (Millions)")
plt.xticks(ticks=[0, 1, 2], labels=['NA Sales', 'EU Sales', 'Global Sales'])
plt.savefig(os.path.join(save_dir, "boxplots.png"))
print("Boxplots saved as boxplots.png")
plt.close()

# Scatter plot (Regional Sales vs. Global Sales)
plt.figure(figsize=(10, 5))
sns.scatterplot(x=df['NA_Sales_Millions'], y=df['Global_Sales_Millions'], label="NA Sales", alpha=0.7)
sns.scatterplot(x=df['EU_Sales_Millions'], y=df['Global_Sales_Millions'], label="EU Sales", alpha=0.7)
plt.xlabel("Regional Sales (Millions)")
plt.ylabel("Global Sales (Millions)")
plt.legend()
plt.title("Regional Sales vs. Global Sales")
plt.grid(True)
plt.savefig(os.path.join(save_dir, "scatterplot.png"))
print("Scatter plot saved as scatterplot.png")
plt.close()
