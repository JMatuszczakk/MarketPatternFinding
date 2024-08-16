import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_data(symbols):
    data = []
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        current_data = ticker.history(period="1d")
        if not current_data.empty:
            latest_price = current_data['Close'].iloc[-1]
            data.append({
                'Symbol': symbol,
                'Price': latest_price,
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    return data

def append_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

def main():
    stocks = [
        'TSLA', 'NKE', 'AMD', 'AMZN', 'NVDA', 'INTC', 'TATAMOTORS.NS', 'DIS', 'PYPL', 'ADBE',
        'V', 'ITC.NS', 'META', 'MA', 'COST', 'HDFCBANK.NS', 'AAPL', 'RELIANCE.NS', 'MSFT', 'MMM',
        'PLTR', 'JPM', 'BRK-A', 'GOOGL', 'BAC', 'JNJ', 'NFLX', 'ABBV', 'KO', 'BABA', 'PFE', 'O'
    ]

    stock_data = fetch_data(stocks)

    filename = f"stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"

    # Append data to CSV
    append_to_csv(stock_data, filename)

    print(f"Data appended to {filename}")

if __name__ == "__main__":
    main()