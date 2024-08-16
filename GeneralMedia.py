import requests
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv()

def get_news_headlines(api_key, country='us', category='general'):
    base_url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        'country': country,
        'category': category,
        'apiKey': api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        
        # Get today's date for the filename
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"news_headlines_{today}.csv"
        
        # Open the file in append mode
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # If the file is empty, write the header
            if os.stat(filename).st_size == 0:
                writer.writerow(['Title', 'Description', 'URL'])
            
            # Write the articles to the CSV file
            for article in articles:
                writer.writerow([
                    article.get('title', ''),
                    article.get('description', ''),
                    article.get('url', '')
                ])
        
        print(f"News headlines have been appended to {filename}")
    else:
        print(f"Error: Unable to fetch news. Status code: {response.status_code}")

if __name__ == "__main__":
    api_key = os.getenv('NEWS_API_KEY')
    
    if not api_key:
        print("Error: NEWS_API_KEY not found in environment variables.")
    else:
        get_news_headlines(api_key)