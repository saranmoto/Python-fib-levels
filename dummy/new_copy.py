# Install necessary packages
# !pip install yfinance matplotlib pandas

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download data using yfinance
symbol = 'SBIN.NS'
df = yf.download(symbol, start='2023-01-01', end='2023-12-31')

# Print the columns to check the correct column name
print(df.columns)

# Ensure 'Close' column exists
if 'Close' not in df.columns:
    raise ValueError("Column 'Close' not found in the data. Please check column names.")

# Calculate Fibonacci retracement levels
Low = df['Close'].min()
High = df['Close'].max()

# Calculate the difference for Fibonacci levels
Diff = High - Low

# Calculate Fibonacci retracement levels
# Fib100 = High.iloc[0] if isinstance(High, pd.Series) else High
# Fib764 = (Low + (Diff * 0.764)).iloc[0] if isinstance(Low + (Diff * 0.764), pd.Series) else Low + (Diff * 0.764)
Fib618 = (Low + (Diff * 0.618)).iloc[0] if isinstance(Low + (Diff * 0.618), pd.Series) else Low + (Diff * 0.618)
Fib58 = (Low + (Diff * 0.58)).iloc[0] if isinstance(Low + (Diff * 0.5), pd.Series) else Low + (Diff * 0.5)
# Fib382 = (Low + (Diff * 0.382)).iloc[0] if isinstance(Low + (Diff * 0.382), pd.Series) else Low + (Diff * 0.382)
# Fib236 = (Low + (Diff * 0.236)).iloc[0] if isinstance(Low + (Diff * 0.236), pd.Series) else Low + (Diff * 0.236)
# Fib0 = Low.iloc[0] if isinstance(Low, pd.Series) else Low


# Print Fibonacci levels
# print(f"Fib100: {Fib100}")
# print(f"Fib764: {Fib764}")
print(f"Fib618: {Fib618}")
print(f"Fib50: {Fib58}")
# print(f"Fib382: {Fib382}")
# print(f"Fib236: {Fib236}")
# print(f"Fib0: {Fib0}")

# Plot the price and Fibonacci retracement levels
plt.figure(figsize=(12, 8))
plt.plot(df['Close'], color="black", label="Price")
# plt.axhline(y=Fib100, color="limegreen", linestyle="-", label="100%")
# plt.axhline(y=Fib764, color="slateblue", linestyle="-", label="76.4%")
plt.axhline(y=Fib618, color="mediumvioletred", linestyle="-", label="61.8%")
plt.axhline(y=Fib58, color="gold", linestyle="-", label="58%")
# plt.axhline(y=Fib236, color="darkturquoise", linestyle="-", label="23.6%")
# plt.axhline(y=Fib0, color="lightcoral", linestyle="-", label="0%")

plt.ylabel("Price")
plt.title(f"{symbol} Fibonacci Retracement Levels")
plt.xticks(rotation=90)
plt.legend()
plt.show()

# Now calculate Fibonacci extensions (for uptrend projection)
# Fib2618 = (High + (Diff * 2.618)).iloc[0] if isinstance(High + (Diff * 2.618), pd.Series) else High + (Diff * 2.618)
# Fib2000 = (High + (Diff * 2)).iloc[0] if isinstance(High + (Diff * 2), pd.Series) else High + (Diff * 2)
Fib1618 = (High + (Diff * 1.618)).iloc[0] if isinstance(High + (Diff * 1.618), pd.Series) else High + (Diff * 1.618)
# Fib1382 = (High + (Diff * 1.382)).iloc[0] if isinstance(High + (Diff * 1.382), pd.Series) else High + (Diff * 1.382)
Fib1272 = (High + (Diff * 1.272)).iloc[0] if isinstance(High + (Diff * 1.272), pd.Series) else High + (Diff * 1.272)
Fib1000 = (High + (Diff * 1)).iloc[0] if isinstance(High + (Diff * 1), pd.Series) else High + (Diff * 1)
# Fib618_ext = (High + (Diff * 0.618)).iloc[0] if isinstance(High + (Diff * 0.618), pd.Series) else High + (Diff * 0.618)

# Print Fibonacci extension levels
# print(f"Fib2618: {Fib2618}")
# print(f"Fib2000: {Fib2000}")
print(f"Fib1618: {Fib1618}")
# print(f"Fib1382: {Fib1382}")
print(f"Fib1272: {Fib1272}")
print(f"Fib1000: {Fib1000}")
# print(f"Fib618_ext: {Fib618_ext}")

# Plot the price and Fibonacci extension levels
plt.figure(figsize=(12, 8))
plt.plot(df['Close'], color="black", label="Price")
# plt.axhline(y=Fib2618, color="darkorange", linestyle="--", label="261.8%")
# plt.axhline(y=Fib2000, color="red", linestyle="--", label="200%")
plt.axhline(y=Fib1618, color="blue", linestyle="--", label="161.8%")
# plt.axhline(y=Fib1382, color="green", linestyle="--", label="138.2%")
plt.axhline(y=Fib1272, color="green", linestyle="--", label="127.2%")
plt.axhline(y=Fib1000, color="purple", linestyle="--", label="100%")
# plt.axhline(y=Fib618_ext, color="brown", linestyle="--", label="61.8%")

plt.ylabel("Price")
plt.title(f"{symbol} Fibonacci Extensions Levels")
plt.xticks(rotation=90)
plt.legend()
plt.show()
