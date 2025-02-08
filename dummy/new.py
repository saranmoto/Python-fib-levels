# Install necessary packages
# !pip install yfinance matplotlib pandas

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go

# Download data using yfinance
symbol = 'SBIN.NS'
df = yf.download(symbol, start='2023-01-01', end='2023-12-31')

# Print the columns to check the correct column name
print(df.columns)

print(df['Open'])

# # Ensure 'Close' column exists
if 'Close' not in df.columns:
    raise ValueError("Column 'Close' not found in the data. Please check column names.")

# # Calculate Fibonacci retracement levels
Low = df['Close'].min()
High = df['Close'].max()

# # Calculate the difference for Fibonacci levels
Diff = High - Low

# # Calculate Fibonacci retracement levels
Fib618 = (Low + (Diff * 0.618)).iloc[0] if isinstance(Low + (Diff * 0.618), pd.Series) else Low + (Diff * 0.618)
Fib58 = (Low + (Diff * 0.58)).iloc[0] if isinstance(Low + (Diff * 0.5), pd.Series) else Low + (Diff * 0.5)

# # Print Fibonacci levels
print(f"Fib618: {Fib618}")
print(f"Fib50: {Fib58}")

# # Plot the price and Fibonacci retracement levels
plt.figure(figsize=(12, 8))
plt.plot(df['Close'], color="black", label="Price")
plt.axhline(y=Fib618, color="mediumvioletred", linestyle="-", label="61.8%")
plt.axhline(y=Fib58, color="gold", linestyle="-", label="58%")

plt.ylabel("Price")
plt.title(f"{symbol} Fibonacci Retracement Levels")
plt.xticks(rotation=90)
plt.legend()
plt.show()

# # Now calculate Fibonacci extensions (for uptrend projection)
Fib1618 = (High + (Diff * 1.618)).iloc[0] if isinstance(High + (Diff * 1.618), pd.Series) else High + (Diff * 1.618)
Fib1272 = (High + (Diff * 1.272)).iloc[0] if isinstance(High + (Diff * 1.272), pd.Series) else High + (Diff * 1.272)
Fib1000 = (High + (Diff * 1)).iloc[0] if isinstance(High + (Diff * 1), pd.Series) else High + (Diff * 1)

print(f"Fib1618: {Fib1618}")
print(f"Fib1272: {Fib1272}")
print(f"Fib1000: {Fib1000}")

# # Plot the price and Fibonacci extension levels
plt.figure(figsize=(12, 8))
plt.plot(df['Close'], color="black", label="Price")
plt.axhline(y=Fib1618, color="blue", linestyle="--", label="161.8%")
plt.axhline(y=Fib1272, color="green", linestyle="--", label="127.2%")
plt.axhline(y=Fib1000, color="purple", linestyle="--", label="100%")

plt.ylabel("Price")
plt.title(f"{symbol} Fibonacci Extensions Levels")
plt.xticks(rotation=90)
plt.legend()
plt.show()