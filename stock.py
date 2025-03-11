import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock data from CSV
@st.cache_data
def fetch_stock_data(file_path):
    return pd.read_csv(file_path)

# Function to calculate a moving average
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

# Input fields
symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL")
file_path = st.text_input("Enter path to your CSV file:", "data/sample_stock_data.csv")

if st.button("Fetch Data"):
    try:
        # Load stock data
        stock_data = fetch_stock_data(file_path)
        
        # Ensure 'Close' column exists
        if 'Close' not in stock_data.columns:
            raise KeyError("CSV file must contain a 'Close' column.")

        # Convert Date column to datetime
        if 'Date' in stock_data.columns:
            stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        else:
            raise KeyError("CSV file must contain a 'Date' column.")

        # Calculate moving averages
        stock_data['SMA_20'] = calculate_moving_average(stock_data['Close'], window=20)
        stock_data['SMA_50'] = calculate_moving_average(stock_data['Close'], window=50)

        # Display stock data
        st.subheader(f"{symbol} Stock Data")
        st.dataframe(stock_data)

        # Plot stock data and moving averages
        st.subheader(f"{symbol} Stock Price and Moving Averages")
        plot_stock_data(stock_data)

    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
    except KeyError as e:
        st.error(f"Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


