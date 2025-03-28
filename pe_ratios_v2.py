from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import matplotlib.pyplot as plt
import time

# List of tickers
tickers = ["AAPL", "MSFT", "GOOGL"]

# Set up Selenium
options = Options()
options.add_argument("--headless")  # Run in headless mode (no browser window)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1200")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Dictionary to store P/E data
pe_data = {}

# Loop through tickers
for ticker in tickers:
    try:
        url = f"https://www.macrotrends.net/stocks/charts/{ticker}/{ticker.lower()}/pe-ratio"
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        # Locate the P/E table by XPath
        rows = driver.find_elements(By.XPATH, '//table[@class="historical_data_table table"]//tr')[1:]

        dates = []
        pe_ratios = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 2:
                dates.append(cols[0].text.strip())
                try:
                    pe_ratios.append(float(cols[1].text.strip().replace(",", "")))
                except ValueError:
                    pe_ratios.append(None)

        # Store data in DataFrame
        pe_data[ticker] = pd.DataFrame({"Date": dates, "P/E Ratio": pe_ratios})
    
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")

# Close the Selenium driver
driver.quit()

# ✅ Plot the P/E ratios
plt.figure(figsize=(12, 6))

for ticker, df in pe_data.items():
    df['Date'] = pd.to_datetime(df['Date'])
    plt.plot(df['Date'], df['P/E Ratio'], label=ticker)

plt.title("P/E Ratios Over Time")
plt.xlabel("Date")
plt.ylabel("P/E Ratio")
plt.legend()
plt.grid(True)
plt.show()
