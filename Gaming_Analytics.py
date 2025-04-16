import streamlit as st
import joblib
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Data/Processed/Final/Merged_Final.csv")  # Path to your data file
    st.write(df.head())  # Check if the data is loaded correctly
    return df

# --- Load model ---
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

# Load data and visualizations
df = load_data()
plots = create_visualizations(df)

# --- Streamlit UI ---
st.title("🎮 Game Sales Analysis & Prediction")

st.subheader("📊 Exploratory Data Analysis")
st.pyplot(plots[0])  # Global Sales Distribution by Genre
st.pyplot(plots[1])  # Global Sales Distribution by Platform
st.pyplot(plots[2])  # Genre Popularity Across Platforms
st.pyplot(plots[3])  # User Score vs Global Sales
st.pyplot(plots[4])  # Price vs Global Sales by Genre
st.pyplot(plots[5])  # Global Sales by Release Season
st.pyplot(plots[6])  # Average Global Sales Over Years

# --- PREDICTION SECTION ---
st.subheader("📈 Predict Game Sales Potential")

# Sample Input UI
col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("Genre", df['Genre'].unique(), key="genre")
    platform = st.selectbox("Platform", df['Platform'].unique(), key="platform")
    price = st.number_input("Price", value=30.0, step=1.0, key="price")

with col2:
    user_score = st.slider("User Score", 0.0, 10.0, 7.5, key="user_score")
    year = st.number_input("Release Year", value=2020, step=1, key="year")

# Load the model
model = load_model()

# Handle preprocessing of input data
if st.button("Predict Sales Potential"):
    # Create the input data as a DataFrame
    input_data = pd.DataFrame([[genre, platform, price, user_score, year]],
                              columns=['Genre', 'Platform', 'Price', 'User_Score', 'Year_of_Release'])
    
    # Fill missing values with a default value
    input_data['Genre'] = input_data['Genre'].fillna('Unknown')
    input_data['Platform'] = input_data['Platform'].fillna('Unknown')

    # Preprocess: encode categorical variables and apply necessary transformations
    input_data_transformed = pd.get_dummies(input_data, columns=['Genre', 'Platform'], drop_first=True)

    # Get the model's feature set
    model_columns = joblib.load("pkl_files/feature_columns.pkl")  # Load the columns used by the model
    
    # Align input data columns with model's feature set
    missing_cols = set(model_columns) - set(input_data_transformed.columns)
    for col in missing_cols:
        input_data_transformed[col] = 0  # Add missing columns with default value

    # Ensure the columns are in the same order as the model
    input_data_transformed = input_data_transformed[model_columns]

    # Predict using the trained model
    sales_prediction = model.predict(input_data_transformed)

    # Display the prediction
    st.header("Prediction Result")
    st.metric("Predicted Global Sales (in millions)", f"${sales_prediction[0]:.2f}M")

# --- Session State Handling for Reduced UI Reset ---
# Store the user inputs persistently to avoid resetting on button press
if "genre" not in st.session_state:
    st.session_state["genre"] = genre
if "platform" not in st.session_state:
    st.session_state["platform"] = platform
if "price" not in st.session_state:
    st.session_state["price"] = price
if "user_score" not in st.session_state:
    st.session_state["user_score"] = user_score
if "year" not in st.session_state:
    st.session_state["year"] = year
