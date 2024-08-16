import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_data(symbols):
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)  # Get data for the last day

    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        history = ticker.history(start=start_date, end=end_date)
        
        if not history.empty:
            latest_data = history.iloc[-1]
            data.append({
                'Symbol': symbol,
                'Timestamp': latest_data.name.strftime('%Y-%m-%d %H:%M:%S'),
                'Open': latest_data['Open'],
                'High': latest_data['High'],
                'Low': latest_data['Low'],
                'Close': latest_data['Close'],
                'Volume': latest_data['Volume'],
                'Dividends': latest_data['Dividends'],
                'Stock Splits': latest_data['Stock Splits']
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
    filename = f"detailed_stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
    append_to_csv(stock_data, filename)
    print(f"Detailed data appended to {filename}")

if __name__ == "__main__":
    main()