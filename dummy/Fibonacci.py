import streamlit as st
import yfinance as yf
import datetime
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def convert_arr(temp):
    array_2d = np.array(temp)
    array_1d = array_2d.flatten()
    array_list = array_1d.tolist()
    return array_list


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

st.sidebar.header('Select Ticker and Date')
today = datetime.date.today()
# Streamlit dropdown
selected_stock = st.sidebar.selectbox("Select a stock ticker", stock_tickers)
# st.write(f"You selected: {selected_stock}")
# Input fields for user to select the stock ticker and date range
# ticker = st.text_input("Enter Stock Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2025-01-01'))
end_date = st.sidebar.date_input("End Date", value=today)
st.header('Fibonacci Retracement & Extension')

try:
    # Fetch stock data
    data = yf.download(selected_stock, start=start_date, end=end_date)

    Low = data['Close'].min()
    High = data['Close'].max()
    Diff = High - Low
    Fib618 = (Low + (Diff * 0.618)).iloc[0] if isinstance(Low + (Diff * 0.618), pd.Series) else Low + (Diff * 0.618)
    Fib58 = (Low + (Diff * 0.58)).iloc[0] if isinstance(Low + (Diff * 0.5), pd.Series) else Low + (Diff * 0.5)
    Fib1618 = (High + (Diff * 1.618)).iloc[0] if isinstance(High + (Diff * 1.618), pd.Series) else High + (Diff * 1.618)
    Fib1272 = (High + (Diff * 1.272)).iloc[0] if isinstance(High + (Diff * 1.272), pd.Series) else High + (Diff * 1.272)
    Fib1000 = (High + (Diff * 1)).iloc[0] if isinstance(High + (Diff * 1), pd.Series) else High + (Diff * 1)
    open_val = convert_arr(data['Open'].values)
    high_val = convert_arr(data['High'].values)
    close_val = convert_arr(data['Close'].values)
    low_val = convert_arr(data['Low'].values)
    date_val = [date.strftime('%Y-%m-%d') for date in data['Open'].index]


    if data.empty:
        st.write("No data available for the entered symbol within the specified date range.")
    else:
        fig = go.Figure(data=[go.Candlestick(x=date_val,
                                             open=open_val,
                                             high=high_val,
                                             low=low_val,
                                             close=close_val)])
        
        # Plot Fibonacci Levels
        fig.add_trace(go.Scatter(x=date_val, y=[Fib58]*len(date_val), mode='lines', name=round(Fib58,2), line=dict(color='orange', dash='dash')))
        fig.add_trace(go.Scatter(x=date_val, y=[Fib618]*len(date_val), mode='lines', name=round(Fib618,2), line=dict(color='blue', dash='dash')))
        fig.add_trace(go.Scatter(x=date_val, y=[Fib1618]*len(date_val), mode='lines', name=round(Fib1618,2), line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=date_val, y=[Fib1272]*len(date_val), mode='lines', name=round(Fib1272,2), line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(x=date_val, y=[Fib1000]*len(date_val), mode='lines', name=round(Fib1000,2), line=dict(color='purple', dash='dash')))


        fig.update_layout(
            title=f'{selected_stock} Candlestick Chart with Fibonacci Levels',
            yaxis_title='Price',
            xaxis_title='Date',
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig)

        fig1 = go.Figure(data=[go.Candlestick(x=date_val,
                                             open=open_val,
                                             high=high_val,
                                             low=low_val,
                                             close=close_val)])
        
        st.plotly_chart(fig1)
except Exception as e:
    st.write(f"An error occurred: {e}")