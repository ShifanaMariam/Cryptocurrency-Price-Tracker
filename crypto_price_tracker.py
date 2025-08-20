from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

#  Headless = False shows browser, True hides it
headless = False

#  Chrome setup
options = Options()
if headless:
    options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

#  Start Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#  Open CoinMarketCap
url = "https://coinmarketcap.com/"
driver.get(url)
time.sleep(5)  # wait for page to load

#  Get top 10 coins
coins = driver.find_elements(By.XPATH, '//table//tbody/tr')[:10]

data = []
for coin in coins:
    try:
        name = coin.find_element(By.XPATH, './td[3]//p').text
        price = coin.find_element(By.XPATH, './td[4]//span').text
        change_24h = coin.find_element(By.XPATH, './td[5]//span').text
        market_cap = coin.find_element(By.XPATH, './td[7]//span').text  # Changed from td[9] to td[7]

        data.append({
            "Name": name,
            "Price": price,
            "24h Change": change_24h,
            "Market Cap": market_cap,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        print(" Error scraping a coin:", e)

#  Done scraping
driver.quit()

#  Create DataFrame
df = pd.DataFrame(data)
print("\n📄 Scraped Data:")
print(df)

#  Save to CSV
csv_file = "crypto_prices.csv"
try:
    old_df = pd.read_csv(csv_file)
    df = pd.concat([old_df, df], ignore_index=True)
except (FileNotFoundError, pd.errors.EmptyDataError):
    pass

df.to_csv(csv_file, index=False)
print(f"\n✅ Data saved to {csv_file}")