import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime

# Functions from previous code remain the same
# ...
# Function to calculate Fibonacci levels
def calculate_fib_levels(start_price, end_price, levels):
    height = abs(start_price - end_price)
    direction = 1 if start_price < end_price else -1
    fib_levels = {}
    for level in levels:
        fib_levels[level] = start_price + direction * height * level
    return fib_levels

def find_last_pivot(data, threshold_multiplier, depth):
    # Convert array values
    high_val = convert_arr(data['High'].values)
    low_val = convert_arr(data['Low'].values)
    close_val = convert_arr(data['Close'].values)
    
    # Calculate ATR using converted arrays
    atr = np.subtract(high_val[-10:], low_val[-10:])
    threshold = np.divide(np.multiply(np.divide(atr, close_val[-10:]), 100), threshold_multiplier)
    
    # Simplified pivot finding logic with converted arrays
    pivots = []
    for i in range(len(high_val)):
        if i > 0 and i < len(high_val) - 1:
            if high_val[i] > high_val[i-1] and high_val[i] > high_val[i+1]:
                pivots.append('High')
            elif low_val[i] < low_val[i-1] and low_val[i] < low_val[i+1]:
                pivots.append('Low')
            else:
                pivots.append('')
        else:
            pivots.append('')
    
    # Find the last pivot within depth
    last_pivots = pivots[-depth:]
    if any(last_pivots):
        last_pivot_index = len(pivots) - depth + last_pivots[::-1].index('High' if 'High' in last_pivots else 'Low') - 1
        last_pivot_type = 'High' if 'High' in last_pivots else 'Low'
        return {
            'type': last_pivot_type, 
            'price': high_val[last_pivot_index] if last_pivot_type == 'High' else low_val[last_pivot_index],
            'time': data.index[last_pivot_index]
        }
    return None

# New function to convert arrays
def convert_arr(temp):
    array_2d = np.array(temp)
    array_1d = array_2d.flatten()
    array_list = array_1d.tolist()
    return array_list

def calculate_pivots(data, depth):
    highs = convert_arr(data['High'].values)
    lows = convert_arr(data['Low'].values)
    pivots_high = []
    pivots_low = []
    
    for i in range(depth, len(highs)):
        if highs[i] >= max(highs[i-depth:i]):
            pivots_high.append((i, highs[i]))
        if lows[i] <= min(lows[i-depth:i]):
            pivots_low.append((i, lows[i]))
    
    return pivots_high, pivots_low

def fib_extension(start, end, levels):
    diff = abs(start - end)
    return {level: end + (level*diff) if start < end else end - (level*diff) for level in levels}

# Streamlit app setup
# List of stock tickers
stock_tickers = [
    "3MINDIA.NS", "AARTIIND.NS", "AAVAS.NS", "ABB.NS", "ABCAPITAL.NS", "ABFRL.NS",
    "ACC.NS", "ADANIENT.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ADANITRANS.NS", "ALKEM.NS",
    "AMARAJABAT.NS", "AMBUJACEM.NS", "APLLTD.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS",
    "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS", "ATUL.NS", "AUBANK.NS", "AUROPHARMA.NS",
    "AVANTIFEED.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS",
    "BALKRISIND.NS", "BALRAMCHIN.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BATAINDIA.NS",
    "BERGEPAINT.NS", "BHARATFORG.NS", "BHARTIARTL.NS", "BHEL.NS", "BIOCON.NS", "BOSCHLTD.NS",
    "BPCL.NS", "BSOFT.NS", "CANFINHOME.NS", "CANBK.NS", "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS",
    "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "COROMANDEL.NS", "CROMPTON.NS", "CUB.NS", "CUMMINSIND.NS",
    "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELTACORP.NS", "DIVISLAB.NS", "DLF.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS", "FEDERALBNK.NS", "GAIL.NS", "GLENMARK.NS", "GMRINFRA.NS",
    "GNFC.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRANULES.NS", "GRASIM.NS", "GSPL.NS", "GUJGASLTD.NS",
    "HAL.NS", "HAVELLS.NS", "HCLTECH.NS", "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS",
    "HINDALCO.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "HINDZINC.NS", "ICICIBANK.NS", "ICICIGI.NS",
    "ICICIPRULI.NS", "IDFCFIRSTB.NS", "IGL.NS", "INDHOTEL.NS", "INDIGO.NS", "INDUSINDBK.NS", "INFY.NS",
    "INTELLECT.NS", "IOC.NS", "IPCALAB.NS", "IRCTC.NS", "ITC.NS", "JINDALSTEL.NS", "JSWSTEEL.NS",
    "JUBLFOOD.NS", "KOTAKBANK.NS", "L&TFH.NS", "LALPATHLAB.NS", "LAURUSLABS.NS", "LICHSGFIN.NS",
    "LT.NS", "LTI.NS", "LTTS.NS", "LUPIN.NS", "M&M.NS", "M&MFIN.NS", "MANAPPURAM.NS", "MARICO.NS",
    "MARUTI.NS", "MCDOWELL-N.NS", "MCX.NS", "METROPOLIS.NS", "MFSL.NS", "MGL.NS", "MINDTREE.NS",
    "MOTHERSON.NS", "MPHASIS.NS", "MRF.NS", "MUTHOOTFIN.NS", "NATIONALUM.NS", "NAUKRI.NS", "NAVINFLUOR.NS",
    "NESTLEIND.NS", "NMDC.NS", "NTPC.NS", "OBEROIRLTY.NS", "OFSS.NS", "ONGC.NS", "PAGEIND.NS", "PEL.NS",
    "PFC.NS", "PIDILITIND.NS", "PIIND.NS", "PNB.NS", "POWERGRID.NS", "PVRINOX.NS", "RAMCOCEM.NS",
    "RBLBANK.NS", "RECLTD.NS", "RELIANCE.NS", "SAIL.NS", "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS",
    "SIEMENS.NS", "SRF.NS", "SRTRANSFIN.NS", "SUNPHARMA.NS", "SUNTV.NS", "SYNGENE.NS", "TATACHEM.NS",
    "TATACOMM.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TECHM.NS",
    "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TVSMOTOR.NS", "UBL.NS", "UJJIVAN.NS", "ULTRACEMCO.NS",
    "UPL.NS", "VOLTAS.NS", "WIPRO.NS", "ZEEL.NS"
]

def check_price_range_inclusion(current_range, fib_levels):
    crossings = []
    low, high = current_range
    for level, fib_price in fib_levels.items():
        if low <= fib_price <= high:
            crossings.append(f"{level} included in today's price range")
    return crossings

def main():
    today = datetime.date.today()

    st.title('Fibonacci Level Crossings for NSE Options Stocks')

    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2025-01-01'))
    end_date = st.sidebar.date_input("End Date", value=today)

    threshold_multiplier = st.sidebar.slider('Deviation', 0.0, 10.0, 3.0, 0.1)
    depth = st.sidebar.slider('Depth', 2, 50, 10, 1)
    reverse = st.sidebar.checkbox('Reverse', value=False)

    results = {}
    
    for stock in stock_tickers:
        data = yf.download(stock, start=start_date, end=end_date)
        if data.empty:
            # results[stock] = "No data available"
            continue

        last_pivot = find_last_pivot(data, threshold_multiplier, depth)
        
        if last_pivot:
            # Fibonacci Retracement levels
            retracement_levels = [0.58, 0.618]
            close_prc = convert_arr(data['Close'].values)
            if reverse:
                start_price, end_price = last_pivot['price'], close_prc[-1]
            else:
                start_price, end_price = close_prc[-1], last_pivot['price']
            retracement_dict = calculate_fib_levels(start_price, end_price, retracement_levels)

            # Fibonacci Extension levels
            pivots_high, pivots_low = calculate_pivots(data, depth)
            if pivots_high and pivots_low:
                last_high = pivots_high[-1]
                last_low = pivots_low[-1]
                is_high_last = last_high[0] > last_low[0]
                start_ext_price = last_low[1] if is_high_last else last_high[1]
                end_ext_price = last_high[1] if is_high_last else last_low[1]
                extension_levels = [1, 1.272, 1.618]
                if reverse:
                    extension_levels = [-x for x in extension_levels]
                extension_dict = fib_extension(start_ext_price, end_ext_price, extension_levels)
            
                # Combine both retracement and extension levels
                all_fib_levels = {**retracement_dict, **extension_dict}
                
                # Check for crossings with last day's prices
                # open_val = convert_arr(data['Open'].values)
                high_val = convert_arr(data['High'].values)
                # close_val = convert_arr(data['Close'].values)
                low_val = convert_arr(data['Low'].values)
                 # Check if today's price range includes any Fibonacci levels
                current_low = low_val[-1]
                current_high = high_val[-1]
                current_range = (current_low, current_high)
                
                inclusions = check_price_range_inclusion(current_range, all_fib_levels)
                if inclusions:
                    results[stock] = inclusions
                # else:
                    # results[stock] = "No Fibonacci levels in today's price range"
            # else:
                # results[stock] = "No pivots found for extensions"
        # else:
            # results[stock] = "No pivot found for retracements"

    # Display results
    for stock, crossings in results.items():
        # st.write(f"**{stock}:** {'; '.join(crossings)}")
        st.write(f"**{stock}**")

if __name__ == "__main__":
    main()