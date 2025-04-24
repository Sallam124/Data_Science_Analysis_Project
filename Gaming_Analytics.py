import streamlit as st
import joblib
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

@st.cache_data
def load_data():
    df = pd.read_csv("Data/Processed/Final/Merged_Final.csv")  # Path to your data file
    st.write(df.head())  # Check if the data is loaded correctly
    return df

@st.cache_resource
def load_model():
    model = joblib.load("pkl_files/linear_model.pkl")  # Path to the saved Linear Regression model
    return model

@st.cache_data
def create_visualizations(df):
    # Convert 'User_Score' and 'Global_Sales_Millions' to numeric
    df['User_Score'] = pd.to_numeric(df['User_Score'], errors='coerce')
    df['Global_Sales_Millions'] = pd.to_numeric(df['Global_Sales_Millions'], errors='coerce')

    # Drop NaNs
    df_clean = df.dropna(subset=['User_Score', 'Global_Sales_Millions'])

    # Plot 1: Global Sales Distribution by Genre
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Genre', y='Global_Sales_Millions', data=df_clean)
    plt.xticks(rotation=45)
    plt.title('Global Sales Distribution by Genre')
    plt.ylabel('Global Sales (Millions)')
    plt.xlabel('Genre')
    genre_sales_plot = plt.gcf()

    # Plot 2: Top Genres by Total Global Sales (Bar Chart)
    genre_totals = df_clean.groupby('Genre')['Global_Sales_Millions'].sum().sort_values(ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=genre_totals.index, y=genre_totals.values, palette='viridis')
    plt.xticks(rotation=45)
    plt.title('Top Genres by Total Global Sales')
    plt.ylabel('Total Global Sales (Millions)')
    plt.xlabel('Genre')
    top_genre_barchart = plt.gcf()

    # Plot 3: Global Sales Distribution by Platform
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Platform', y='Global_Sales_Millions', data=df_clean)
    plt.xticks(rotation=45)
    plt.title('Global Sales Distribution by Platform')
    plt.ylabel('Global Sales (Millions)')
    plt.xlabel('Platform')
    platform_sales_plot = plt.gcf()

    # Plot 4: Genre Popularity Across Platforms (Heatmap)
    genre_platform_pivot = df_clean.pivot_table(index='Genre', columns='Platform', values='Global_Sales_Millions', aggfunc='sum').fillna(0)
    plt.figure(figsize=(14, 8))
    sns.heatmap(genre_platform_pivot, cmap='YlGnBu', annot=True, fmt='.1f')
    plt.title('Genre Popularity Across Platforms (Total Global Sales)')
    plt.xlabel('Platform')
    plt.ylabel('Genre')
    genre_platform_heatmap = plt.gcf()

    # Plot 5: User Score vs Global Sales
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='User_Score', y='Global_Sales_Millions', data=df_clean, alpha=0.6)
    sns.regplot(x='User_Score', y='Global_Sales_Millions', data=df_clean, scatter=False, color='red')
    plt.title('User Score vs Global Sales')
    plt.xlabel('User Score')
    plt.ylabel('Global Sales (Millions)')
    user_score_sales_plot = plt.gcf()

    # Plot 6: Price vs Global Sales by Genre
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Price', y='Global_Sales_Millions', data=df_clean, hue='Genre', alpha=0.7)
    plt.title('Price vs Global Sales by Genre')
    plt.xlabel('Price ($)')
    plt.ylabel('Global Sales (Millions)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    price_sales_plot = plt.gcf()

    # Plot 7: Global Sales by Release Season
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Release_Season', y='Global_Sales_Millions', data=df_clean)
    plt.title('Global Sales by Release Season')
    plt.ylabel('Global Sales (Millions)')
    plt.xlabel('Release Season')
    release_season_sales_plot = plt.gcf()

    # Plot 8: Average Global Sales Over Years
    year_sales = df_clean.groupby('Year_of_Release')['Global_Sales_Millions'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=year_sales, x='Year_of_Release', y='Global_Sales_Millions', marker='o')
    plt.title('Average Global Sales Over Years')
    plt.xlabel('Year of Release')
    plt.ylabel('Avg Global Sales (Millions)')
    year_sales_plot = plt.gcf()

    return (
        genre_sales_plot,
        top_genre_barchart,
        platform_sales_plot,
        genre_platform_heatmap,
        user_score_sales_plot,
        price_sales_plot,
        release_season_sales_plot,
        year_sales_plot
    )


df = load_data()
plots = create_visualizations(df)

# --- Streamlit UI ---
st.title("🎮 Game Sales Analysis & Prediction")

# Exploratory Data Analysis Section
st.subheader("📊 Exploratory Data Analysis")
st.pyplot(plots[0])  # Global Sales Distribution by Genre
st.pyplot(plots[1])  # Global Sales Distribution by Platform
st.pyplot(plots[2])  # Genre Popularity Across Platforms
st.pyplot(plots[3])  # User Score vs Global Sales
st.pyplot(plots[4])  # Price vs Global Sales by Genre
st.pyplot(plots[5])  # Global Sales by Release Season
st.pyplot(plots[6])  # Average Global Sales Over Years

# --- Mappings ---
genre_mapping = {0: "Action", 1: "Sports", 2: "Shooter", 3: "RPG", 4: "Fighting", 5: "Strategy", 6: "Adventure", 7: "Puzzle", 8: "Racing", 9: "Simulation", 10: "Platform", 11: "Other"}
platform_mapping = {0: "Wii", 1: "PS4", 2: "PS3", 3: "PS2", 4: "Xbox One", 5: "Xbox 360", 6: "Xbox", 7: "PC", 8: "3DS", 9: "PSP", 10: "DS", 11: "PS Vita", 12: "NES", 13: "SNES", 14: "N64", 15: "Game Boy", 16: "Game Boy Color", 17: "GameCube", 18: "Dreamcast", 19: "Saturn", 20: "PC Engine", 21: "Neo Geo", 22: "Wii U", 23: "PSP Go", 24: "Virtual Boy", 25: "3DO"}
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

st.subheader("📈 Predict Game Sales Potential")

# Sample Input UI
col1, col2 = st.columns(2)

with col1:
    genre = st.selectbox("Genre", list(genre_mapping.values()), key="genre")
    platform = st.selectbox("Platform", list(platform_mapping.values()), key="platform")
    price = st.slider('Price', min_value=0.0, max_value=99.99, step=0.10, key="price")  

with col2:
    user_score = st.slider("User Score", 0.0, 10.0, 7.5, key="user_score")
    release_year = st.slider("Release Year", 1980, 2035, 2000, key="release_year")  
    release_season = st.selectbox("Release Season", list(season_mapping.values()), key="release_season")

# Load the model
model = load_model()

# Handle preprocessing of input data
if st.button("Predict Sales Potential"):
    genre_numeric = {v: k for k, v in genre_mapping.items()}[genre]
    platform_numeric = {v: k for k, v in platform_mapping.items()}[platform]
    release_season_numeric = {v: k for k, v in season_mapping.items()}[release_season]

    scaler = MinMaxScaler()
    price_normalized = price / 99.99
    year_normalized = (release_year - 1980) / (2030 - 1980)

    input_data = pd.DataFrame([[genre_numeric, platform_numeric, release_season_numeric, price_normalized, user_score, year_normalized]], 
                              columns=['Genre', 'Platform', 'Release_Season', 'Price', 'User_Score', 'Year_of_Release'])

    input_data['Genre'] = input_data['Genre'].fillna(0)
    input_data['Platform'] = input_data['Platform'].fillna(0)
    input_data['Release_Season'] = input_data['Release_Season'].fillna(1)
    input_data['Price'] = input_data['Price'].fillna(0.5)
    input_data['User_Score'] = input_data['User_Score'].fillna(5.0)
    input_data['Year_of_Release'] = input_data['Year_of_Release'].fillna(0.5)

    input_data = pd.get_dummies(input_data, drop_first=True)


    prediction = model.predict(input_data)
    st.header("Prediction Result")
    st.metric("Predicted Global Sales (in millions)", f"${prediction[0]:.2f}M")
