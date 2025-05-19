import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://housestockwatcher.com"
DATA_URL = f"{BASE_URL}/trades"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_trade_data(page=1):
    url = f"{DATA_URL}?page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")[1:]  # Skip header row

    data = []
    for row in rows:
        cols = row.find_all("td")
        trade = {
            "Date": cols[0].text.strip(),
            "Representative": cols[1].text.strip(),
            "Ticker": cols[2].text.strip(),
            "Asset": cols[3].text.strip(),
            "Type": cols[4].text.strip(),
            "Amount": cols[5].text.strip(),
            "Owner": cols[6].text.strip(),
        }
        data.append(trade)
    return data

def scrape_multiple_pages(pages=5, delay=1):
    all_data = []
    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        trades = get_trade_data(page)
        all_data.extend(trades)
        time.sleep(delay)  # Be respectful of their server
    return all_data

# Run the scraper
pages_to_scrape = 10  # Change this to get more data
scraped_data = scrape_multiple_pages(pages=pages_to_scrape)

# Save to CSV
df = pd.DataFrame(scraped_data)
df.to_csv("congressional_trading_data.csv", index=False)
print("Saved data to congressional_trading_data.csv")
