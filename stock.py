import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to read uploaded CSV file
@st.cache_data
def load_stock_data(uploaded_file):
    return pd.read_csv(uploaded_file)

# Function to calculate moving average
def calculate_moving_average(data, window):
    return data.rolling(window=window).mean()

# Function to plot stock data
def plot_stock_data(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['Date'], df['Close'], label="Close Price", color='blue')
    ax.plot(df['Date'], df['SMA_20'], label="20-day SMA", color='red')
    ax.plot(df['Date'], df['SMA_50'], label="50-day SMA", color='green')
    
    ax.set_xlabel("Date")
    ax.set_ylabel("Stock Price")
    ax.set_title("Stock Price Trend")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Streamlit UI
st.set_page_config(page_title="Stock Trend Analyzer", layout="wide")
st.title("📈 Stock Trend Analyzer")

# File uploader instead of manual file path
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load stock data
        stock_data = load_stock_data(uploaded_file)

        # Ensure required columns exist
        if 'Date' not in stock_data.columns or 'Close' not in stock_data.columns:
            st.error("CSV file must contain 'Date' and 'Close' columns.")
        else:
            # Convert Date column to datetime
            stock_data['Date'] = pd.to_datetime(stock_data['Date'])

            # Calculate moving averages
            stock_data['SMA_20'] = calculate_moving_average(stock_data['Close'], window=20)
            stock_data['SMA_50'] = calculate_moving_average(stock_data['Close'], window=50)

            # Display stock data
            st.subheader("Stock Data")
            st.dataframe(stock_data)

            # Plot stock data
            st.subheader("Stock Price and Moving Averages")
            plot_stock_data(stock_data)

    except Exception as e:
        st.error(f"An error occurred: {e}")
