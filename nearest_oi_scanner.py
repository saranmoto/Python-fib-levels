import requests
import sys
import pandas
from typing import Optional, Dict, Any, List


class StockOptionChainFetcher:
    def __init__(self):
        self.url_oc: str = "https://www.nseindia.com/option-chain"
        self.url_stock: str = "https://www.nseindia.com/api/option-chain-equities?symbol="
        self.headers: Dict[str, str] = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/130.0.0.0 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://www.nseindia.com/option-chain'
        }
        self.session: requests.Session = requests.Session()
        self.cookies: Dict[str, str] = {}

    def initialize_session(self) -> bool:
        try:
            request: requests.Response = self.session.get(self.url_oc, headers=self.headers, timeout=5)
            request.raise_for_status()
            self.cookies = dict(request.cookies)
            return True
        except requests.exceptions.RequestException as err:
            print(f"Error initializing session: {err}, {sys.exc_info()[0]}")
            return False

    def fetch_stock_option_chain(self, stock_symbol: str) -> Optional[Dict[str, Any]]:
        if not self.cookies:
            if not self.initialize_session():
                print("Failed to initialize session. Please try again.")
                return None

        url: str = self.url_stock + stock_symbol
        try:
            response: requests.Response = self.session.get(url, headers=self.headers, timeout=5, cookies=self.cookies)
            print(f"Response Status Code for {stock_symbol}: {response.status_code}")
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f"Error fetching data for {stock_symbol}: {err}")
            return None

        try:
            print(f"Response  {response.text[:500]}")
            json_data: Dict[str, Any] = response.json()
        except ValueError as err:
            print(f"Error parsing JSON for {stock_symbol}: {err}")
            return None

        try:
            all_data = json_data['records']['data']
            expiry_dates = json_data['records']['expiryDates']
            close_price = json_data['records']['underlyingValue']

            if not expiry_dates:
                return None

            nearest_expiry = expiry_dates[0]
            filtered_data = [item for item in all_data if item.get('expiryDate') == nearest_expiry]

            ce_values = [data['CE'] for data in filtered_data if "CE" in data]
            pe_values = [data['PE'] for data in filtered_data if "PE" in data]

            ce_data_f = pandas.DataFrame(ce_values)
            pe_data_f = pandas.DataFrame(pe_values)

            if ce_data_f.empty or pe_data_f.empty:
                return None

            max_call_oi = ce_data_f.loc[ce_data_f['openInterest'].idxmax()]
            max_put_oi = pe_data_f.loc[pe_data_f['openInterest'].idxmax()]

            call_strike = max_call_oi['strikePrice']
            put_strike = max_put_oi['strikePrice']

            # Corrected nearest logic
            call_diff = abs(close_price - call_strike)
            put_diff = abs(close_price - put_strike)

            if call_strike == put_strike:
                nearest = "both"
            elif call_diff < put_diff:
                nearest = "call"
            elif put_diff < call_diff:
                nearest = "put"
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
            print(f"Error processing JSON data for {stock_symbol}: {err}")
            return None

    def close_session(self) -> None:
        self.session.close()

    @staticmethod
    def create_instance_for_list(stock_symbols: List[str]) -> None:
        fetcher = StockOptionChainFetcher()
        all_data = []

        for symbol in stock_symbols:
            data = fetcher.fetch_stock_option_chain(symbol)
            if data:
                close = data['close_price']
                call = data['highest_call_oi_strike']
                put = data['highest_put_oi_strike']
                # Filtering condition: within +/- 2% of call or put strike
                in_range = (
                    abs(close - call) <= 0.001 * call or
                    abs(close - put) <= 0.001 * put
                )
                if in_range:
                    all_data.append(data)

        fetcher.close_session()

        if all_data:
            print(f"\n{'Symbol':<10} | {'Close Price':<12} | {'Call OI Strike':<15} | {'Put OI Strike':<14} | Nearest")
            print("-" * 70)
            for d in all_data:
                print(f"{d['symbol']:<10} | {d['close_price']:<12.2f} | {d['highest_call_oi_strike']:<15} | "
                      f"{d['highest_put_oi_strike']:<14} | {d['nearest']}")
        else:
            print("No stocks matched the filter criteria.")


if __name__ == '__main__':
    stock_list = [
        'ABB'
        # , 'ACC', 'APLAPOLLO', 'AUBANK', 'AARTIIND', 'ADANIENSOL', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ATGL',
        # 'ABCAPITAL', 'ABFRL', 'ALKEM', 'AMBUJACEM', 'ANGELONE', 'APOLLOHOSP', 'APOLLOTYRE', 'ASHOKLEY', 'ASIANPAINT',
        # 'ASTRAL', 'AUROPHARMA', 'DMART', 'AXISBANK', 'BSOFT', 'BSE', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV',
        # 'BALKRISIND', 'BANDHANBNK', 'BANKBARODA', 'BANKINDIA', 'BEL', 'BHARATFORG', 'BHEL', 'BPCL',
        # 'BHARTIARTL', 'BIOCON', 'BOSCHLTD', 'BRITANNIA', 'CESC', 'CGPOWER', 'CANBK', 'CDSL', 'CHAMBLFERT', 'CHOLAFIN',
        # 'CIPLA', 'COALINDIA', 'COFORGE', 'COLPAL', 'CAMS', 'CONCOR', 'CROMPTON', 'CUMMINSIND', 'CYIENT', 'DLF',
        # 'DABUR', 'DALBHARAT', 'DEEPAKNTR', 'DELHIVERY', 'DIVISLAB', 'DIXON', 'DRREDDY', 'ETERNAL', 'EICHERMOT',
        # 'ESCORTS', 'EXIDEIND', 'NYKAA', 'GAIL', 'GMRAIRPORT', 'GLENMARK', 'GODREJCP', 'GODREJPROP', 'GRANULES',
        # 'GRASIM', 'HCLTECH', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HFCL', 'HAVELLS', 'HEROMOTOCO', 'HINDALCO', 'HAL',
        # 'HINDCOPPER', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'HUDCO', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI',
        # 'IDFCFIRSTB', 'IIFL', 'IRB', 'ITC', 'INDIANB', 'IEX', 'IOC', 'IRCTC', 'IRFC', 'IREDA', 'IGL', 'INDUSTOWER',
        # 'INDUSINDBK', 'NAUKRI', 'INFY', 'INOXWIND', 'INDIGO', 'JSWENERGY', 'JSWSTEEL', 'JSL', 'JINDALSTEL', 'JIOFIN',
        # 'JUBLFOOD', 'KEI', 'KPITTECH', 'KALYANKJIL', 'KOTAKBANK', 'LTF', 'LICHSGFIN', 'LTIM', 'LT', 'LAURUSLABS',
        # 'LICI', 'LUPIN', 'MRF', 'LODHA', 'MGL', 'M%26MFIN', 'M%26M', 'MANAPPURAM', 'MARICO', 'MARUTI', 'MFSL',
        # 'MAXHEALTH', 'MPHASIS', 'MCX', 'MUTHOOTFIN', 'NBCC', 'NCC', 'NHPC', 'NMDC', 'NTPC', 'NATIONALUM',
        # 'NESTLEIND', 'OBEROIRLTY', 'ONGC', 'OIL', 'PAYTM', 'OFSS', 'POLICYBZR', 'PIIND', 'PNBHOUSING', 'PAGEIND',
        # 'PATANJALI', 'PERSISTENT', 'PETRONET', 'PIDILITIND', 'PEL', 'POLYCAB', 'POONAWALLA', 'PFC', 'POWERGRID',
        # 'PRESTIGE', 'PNB', 'RBLBANK', 'RECLTD', 'RELIANCE', 'SBICARD', 'SBILIFE', 'SHREECEM', 'SJVN', 'SRF',
        # 'MOTHERSON', 'SHRIRAMFIN', 'SIEMENS', 'SOLARINDS', 'SONACOMS', 'SBIN', 'SAIL', 'SUNPHARMA', 'SUPREMEIND',
        # 'SYNGENE', 'TATACONSUM', 'TITAGARH', 'TVSMOTOR', 'TATACHEM', 'TATACOMM', 'TCS', 'TATAELXSI', 'TATAMOTORS',
        # 'TATAPOWER', 'TATASTEEL', 'TATATECH', 'TECHM', 'FEDERALBNK', 'INDHOTEL', 'PHOENIXLTD', 'RAMCOCEM', 'TITAN',
        # 'TORNTPHARM', 'TORNTPOWER', 'TRENT', 'TIINDIA', 'UPL', 'ULTRACEMCO', 'UNIONBANK', 'UNITDSPR', 'VBL',
        # 'VEDL', 'IDEA', 'VOLTAS', 'WIPRO', 'YESBANK', 'ZYDUSLIFE'
        ]
    
    StockOptionChainFetcher.create_instance_for_list(stock_list)
