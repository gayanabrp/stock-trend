import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from main import fetch_stock_data
from analysis import calculate_moving_average
from visualization import plot_stock_data

st.set_page_config(page_title="Stock Trend Analyzer", layout="wide")

# Title
st.title("📈 Stock Trend Analyzer")

# Input fields
symbol = st.text_input("Enter stock symbol (e.g., AAPL):", "AAPL")
file_path = st.text_input("Enter path to your CSV file:", "data/sample_stock_data.csv")

if st.button("Fetch Data"):
    try:
        # Fetch stock data
        stock_data = fetch_stock_data(file_path)

        # Compute moving averages
        stock_data['SMA_20'] = calculate_moving_average(stock_data['Close'], window=20)
        stock_data['SMA_50'] = calculate_moving_average(stock_data['Close'], window=50)

        # Display Data
        st.subheader(f"{symbol} Stock Data")
        st.dataframe(stock_data)

        # Visualization
        st.subheader(f"{symbol} Stock Price and Moving Averages")
        fig, ax = plt.subplots(figsize=(12, 6))
        plot_stock_data(stock_data, ax)
        st.pyplot(fig)

    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
    except KeyError as e:
        st.error(f"Error: {e}. Ensure 'Close' column exists in the dataset.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

