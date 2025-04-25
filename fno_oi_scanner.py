import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
import requests

class StockOptionChainFetcher:
    def __init__(self):
        self.url_oc: str = "https://www.nseindia.com/option-chain"
        self.url_stock: str = "https://www.nseindia.com/api/option-chain-equities?symbol="
        self.headers: Dict[str, str] = {
            'user-agent': 'Mozilla/5.0',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://www.nseindia.com/option-chain'
        }
        self.session: requests.Session = requests.Session()
        self.cookies: Dict[str, str] = {}

    def initialize_session(self) -> bool:
        try:
            request = self.session.get(self.url_oc, headers=self.headers, timeout=120)
            request.raise_for_status()
            self.cookies = dict(request.cookies)
            return True
        except requests.exceptions.RequestException as err:
            st.error(f"Error initializing session: {err}")
            return False

    def fetch_stock_option_chain(self, stock_symbol: str) -> Optional[Dict[str, Any]]:
        if not self.cookies and not self.initialize_session():
            return None

        url = self.url_stock + stock_symbol
        try:
            response = self.session.get(url, headers=self.headers, timeout=120, cookies=self.cookies)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            st.warning(f"Error fetching data for {stock_symbol}: {err}")
            return None

        try:
            json_data = response.json()
            all_data = json_data['records']['data']
            expiry_dates = json_data['records']['expiryDates']
            close_price = json_data['records']['underlyingValue']

            if not expiry_dates:
                return None

            nearest_expiry = expiry_dates[0]
            filtered_data = [item for item in all_data if item.get('expiryDate') == nearest_expiry]

            ce_values = [data['CE'] for data in filtered_data if "CE" in data]
            pe_values = [data['PE'] for data in filtered_data if "PE" in data]

            ce_data_f = pd.DataFrame(ce_values)
            pe_data_f = pd.DataFrame(pe_values)

            if ce_data_f.empty or pe_data_f.empty:
                return None

            max_call_oi = ce_data_f.loc[ce_data_f['openInterest'].idxmax()]
            max_put_oi = pe_data_f.loc[pe_data_f['openInterest'].idxmax()]

            call_strike = max_call_oi['strikePrice']
            put_strike = max_put_oi['strikePrice']

            call_diff = abs(close_price - call_strike)
            put_diff = abs(close_price - put_strike)

            if call_strike == put_strike:
                nearest = "Both"
            elif call_diff < put_diff:
                nearest = "CALL"
            elif put_diff < call_diff:
                nearest = "PUT"
            else:
                nearest = "both"

            return {
                'symbol': stock_symbol,
                'close_price': close_price,
                'highest_call_oi_strike': call_strike,
                'highest_put_oi_strike': put_strike,
                'nearest': nearest
            }
        except Exception as err:
            st.error(f"Error processing data for {stock_symbol}: {err}")
            return None

    def close_session(self):
        self.session.close()

def main():
    st.title("NSE - FNO Stock Near Highest OI")

    stock_list = st.text_area("Enter comma-separated stock symbols:", value="ABB, ACC, APLAPOLLO, AUBANK, AARTIIND, ADANIENSOL, ADANIENT, ADANIGREEN, ADANIPORTS, ATGL, ABCAPITAL, ABFRL, ALKEM, AMBUJACEM, ANGELONE, APOLLOHOSP, APOLLOTYRE, ASHOKLEY, ASIANPAINT, ASTRAL, AUROPHARMA, DMART, AXISBANK, BSOFT, BSE, BAJAJ-AUTO, BAJFINANCE, BAJAJFINSV, BALKRISIND, BANDHANBNK, BANKBARODA, BANKINDIA, BEL, BHARATFORG, BHEL, BPCL, BHARTIARTL, BIOCON, BOSCHLTD, BRITANNIA, CESC, CGPOWER, CANBK, CDSL, CHAMBLFERT, CHOLAFIN, CIPLA, COALINDIA, COFORGE, COLPAL, CAMS, CONCOR, CROMPTON, CUMMINSIND, CYIENT, DLF, DABUR, DALBHARAT, DEEPAKNTR, DELHIVERY, DIVISLAB, DIXON, DRREDDY, ETERNAL, EICHERMOT, ESCORTS, EXIDEIND, NYKAA, GAIL, GMRAIRPORT, GLENMARK, GODREJCP, GODREJPROP, GRANULES, GRASIM, HCLTECH, HDFCAMC, HDFCBANK, HDFCLIFE, HFCL, HAVELLS, HEROMOTOCO, HINDALCO, HAL, HINDCOPPER, HINDPETRO, HINDUNILVR, HINDZINC, HUDCO, ICICIBANK, ICICIGI, ICICIPRULI, IDFCFIRSTB, IIFL, IRB, ITC, INDIANB, IEX, IOC, IRCTC, IRFC, IREDA, IGL, INDUSTOWER, INDUSINDBK, NAUKRI, INFY, INOXWIND, INDIGO, JSWENERGY, JSWSTEEL, JSL, JINDALSTEL, JIOFIN, JUBLFOOD, KEI, KPITTECH, KALYANKJIL, KOTAKBANK, LTF, LICHSGFIN, LTIM, LT, LAURUSLABS, LICI, LUPIN, MRF, LODHA, MGL, M%26MFIN, M%26M, MANAPPURAM, MARICO, MARUTI, MFSL, MAXHEALTH, MPHASIS, MCX, MUTHOOTFIN, NBCC, NCC, NHPC, NMDC, NTPC, NATIONALUM, NESTLEIND, OBEROIRLTY, ONGC, OIL, PAYTM, OFSS, POLICYBZR, PIIND, PNBHOUSING, PAGEIND, PATANJALI, PERSISTENT, PETRONET, PIDILITIND, PEL, POLYCAB, POONAWALLA, PFC, POWERGRID, PRESTIGE, PNB, RBLBANK, RECLTD, RELIANCE, SBICARD, SBILIFE, SHREECEM, SJVN, SRF, MOTHERSON, SHRIRAMFIN, SIEMENS, SOLARINDS, SONACOMS, SBIN, SAIL, SUNPHARMA, SUPREMEIND, SYNGENE, TATACONSUM, TITAGARH, TVSMOTOR, TATACHEM, TATACOMM, TCS, TATAELXSI, TATAMOTORS, TATAPOWER, TATASTEEL, TATATECH, TECHM, FEDERALBNK, INDHOTEL, PHOENIXLTD, RAMCOCEM, TITAN, TORNTPHARM, TORNTPOWER, TRENT, TIINDIA, UPL, ULTRACEMCO, UNIONBANK, UNITDSPR, VBL, VEDL, IDEA, VOLTAS, WIPRO, YESBANK, ZYDUSLIFE").split(',')
    stock_list = [s.strip().upper() for s in stock_list if s.strip()]
    percentage_range = st.slider("Percentage range from OI strike", 0.1, 5.0, 0.5, step=0.1)

    if st.button("Fetch Open Interest Data"):
        fetcher = StockOptionChainFetcher()
        all_data = []

        with st.spinner("Fetching data..."):
            for symbol in stock_list:
                data = fetcher.fetch_stock_option_chain(symbol)
                if data:
                    close = data['close_price']
                    call = data['highest_call_oi_strike']
                    put = data['highest_put_oi_strike']
                    in_range = (
                        abs(close - call) <= (percentage_range / 100) * call or
                        abs(close - put) <= (percentage_range / 100) * put
                    )
                    if in_range:
                        all_data.append(data)

            fetcher.close_session()

        if all_data:
            df = pd.DataFrame(all_data)
            st.dataframe(df)
        else:
            st.info("No stocks matched the filter criteria.")

if __name__ == "__main__":
    main()
