import requests
import matplotlib.pyplot as plt
import pandas as pd
import time

# Alpha Vantage API key (replace with your own key)
API_KEY = "W3PV4DCRJWZOQNZB"

# List of top 50 S&P 500 companies' tickers (add more if needed)
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "BRK.B", "NVDA", "META",
    "JPM", "UNH", "V", "XOM", "PG", "JNJ", "HD", "MA",
    "CVX", "LLY", "ABBV", "PFE", "PEP", "KO", "MRK", "TMO",
    "COST", "MCD", "DIS", "NFLX", "ADBE", "PYPL", "CRM", "INTC",
    "CSCO", "ACN", "AVGO", "TXN", "AMD", "AMGN", "QCOM", "LMT",
    "NKE", "LOW", "CAT", "GS", "RTX", "BA", "HON", "IBM", "ORCL", "NOW"
]

# Dictionary to store P/E ratios
pe_ratios = {}

# Function to fetch P/E ratio using Alpha Vantage
def get_pe_ratio(ticker, api_key):
    try:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
        response = requests.get(url).json()
        
        pe_ratio = response.get("PERatio")
        if pe_ratio and pe_ratio != "None":
            return float(pe_ratio)
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return None
    return None

# Fetch P/E ratios with a delay to avoid rate limiting
for i, ticker in enumerate(tickers):
    pe = get_pe_ratio(ticker, API_KEY)
    
    if pe:
        pe_ratios[ticker] = pe

    print(f"{i+1}/{len(tickers)}: {ticker} - P/E: {pe}")
    
    # Alpha Vantage free tier allows 5 requests per minute → add delay
    if (i + 1) % 5 == 0:
        print("Pausing for 60 seconds to avoid rate limit...")
        time.sleep(60)

# Convert to DataFrame
pe_df = pd.DataFrame(pe_ratios.items(), columns=["Company", "P/E Ratio"])
pe_df = pe_df.sort_values(by="P/E Ratio", ascending=False)

# Plot the P/E ratios
plt.figure(figsize=(15, 6))
plt.bar(pe_df["Company"], pe_df["P/E Ratio"], color="skyblue")
plt.xticks(rotation=90)
plt.xlabel("Company")
plt.ylabel("P/E Ratio")
plt.title("P/E Ratios of the Top 50 S&P 500 Companies")
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.show()
