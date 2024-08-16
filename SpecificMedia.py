import requests
import os
import csv
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Dictionary mapping stock symbols to full company names
COMPANY_NAMES = {
    'TSLA': 'Tesla',
    'NKE': 'Nike',
    'AMD': 'Advanced Micro Devices',
    'AMZN': 'Amazon',
    'NVDA': 'NVIDIA',
    'INTC': 'Intel',
    'TATAMOTORS.NS': 'Tata Motors',
    'DIS': 'Disney',
    'PYPL': 'PayPal',
    'ADBE': 'Adobe',
    'V': 'Visa',
    'ITC.NS': 'ITC Limited',
    'META': 'Meta Platforms',
    'MA': 'Mastercard',
    'COST': 'Costco',
    'HDFCBANK.NS': 'HDFC Bank',
    'AAPL': 'Apple',
    'RELIANCE.NS': 'Reliance Industries',
    'MSFT': 'Microsoft',
    'MMM': '3M',
    'PLTR': 'Palantir Technologies',
    'JPM': 'JPMorgan Chase',
    'BRK-A': 'Berkshire Hathaway',
    'GOOGL': 'Alphabet',
    'BAC': 'Bank of America',
    'JNJ': 'Johnson & Johnson',
    'NFLX': 'Netflix',
    'ABBV': 'AbbVie',
    'KO': 'Coca-Cola',
    'BABA': 'Alibaba',
    'PFE': 'Pfizer',
    'O': 'Realty Income Corporation'
}

def get_stock_news(api_key, symbols, days=1):
    base_url = "https://newsapi.org/v2/everything"
    
    # Calculate the date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Create a CSV file for today's date
    csv_filename = f"stock_news_{end_date.strftime('%Y-%m-%d')}.csv"
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Date', 'Symbol', 'Company', 'Title', 'Published At', 'URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
    
        for symbol in symbols:
            company_name = COMPANY_NAMES.get(symbol, symbol)
            query = f'"{symbol}" OR "{company_name}"'
            
            params = {
                'q': query,
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'language': 'en',
                'apiKey': api_key
            }
            
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                news_data = response.json()
                articles = news_data.get('articles', [])
                
                print(f"\nNews for {symbol} ({company_name}):")
                for i, article in enumerate(articles[:5], 1):  # Limit to top 5 articles
                    print(f"{i}. {article['title']}")
                    print(f"   Published at: {article['publishedAt']}")
                    print(f"   URL: {article['url']}\n")
                    
                    # Write to CSV
                    writer.writerow({
                        'Date': end_date.strftime('%Y-%m-%d'),
                        'Symbol': symbol,
                        'Company': company_name,
                        'Title': article['title'],
                        'Published At': article['publishedAt'],
                        'URL': article['url']
                    })
            else:
                print(f"Error: Unable to fetch news for {symbol} ({company_name}). Status code: {response.status_code}")

if __name__ == "__main__":
    api_key = os.getenv('NEWS_API_KEY')
    
    if not api_key:
        print("Error: NEWS_API_KEY not found in environment variables.")
    else:
        symbols = list(COMPANY_NAMES.keys())
        get_stock_news(api_key, symbols)