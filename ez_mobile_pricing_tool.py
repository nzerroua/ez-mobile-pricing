import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
from datetime import datetime

# Create output directory
OUTPUT_DIR = "pricing_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_price(price_str):
    try:
        price = re.sub(r"[^0-9.]", "", price_str)
        return float(price)
    except:
        return None

def extract_details(title):
    title = title.lower()
    model = ""
    storage = ""
    lock_status = "unlocked" if "unlocked" in title else ("locked" if "locked" in title else "unknown")

    if "pro max" in title:
        model = "iphone 13 pro max"
    elif "pro" in title:
        model = "iphone 13 pro"
    elif "mini" in title:
        model = "iphone 13 mini"
    else:
        model = "iphone 13"

    if "128" in title:
        storage = "128GB"
    elif "256" in title:
        storage = "256GB"
    elif "512" in title:
        storage = "512GB"
    else:
        storage = "unknown"

    return model, storage, lock_status

def is_valid_title(title):
    title = title.lower()
    return ("iphone" in title and "13" in title and not any(bad in title for bad in ["shop", "ad", "sponsored", "lot"]))

def scrape_ebay(query="iPhone 13", pages=4):
    listings = []
    for p in range(1, pages + 1):
        url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}&_pgn={p}"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select(".s-item"):
            title = item.select_one(".s-item__title")
            price = item.select_one(".s-item__price")
            cond = item.select_one(".SECONDARY_INFO")
            link = item.select_one("a.s-item__link")
            if title and price and is_valid_title(title.text):
                model, storage, lock_status = extract_details(title.text)
                listings.append({
                    "source": "ebay",
                    "model": model,
                    "storage": storage,
                    "lock_status": lock_status,
                    "price": clean_price(price.text),
                    "condition": cond.text.strip() if cond else None,
                    "url": link["href"] if link else None,
                    "timestamp": pd.Timestamp.now()
                })
        time.sleep(1)
    return pd.DataFrame(listings)

def scrape_swappa_prices():
    url = "https://swappa.com/prices"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = []
    for row in soup.select("table tbody tr"):
        cols = row.find_all("td")
        if len(cols) >= 3:
            model_text = cols[0].text.strip().lower()
            avg_price = clean_price(cols[2].text.strip())
            if "iphone" in model_text and "13" in model_text:
                model, storage, lock_status = extract_details(model_text)
                data.append({
                    "source": "swappa",
                    "model": model,
                    "storage": storage,
                    "lock_status": lock_status,
                    "price": avg_price,
                    "condition": "avg",
                    "url": "https://swappa.com/prices",
                    "timestamp": pd.Timestamp.now()
                })
    return pd.DataFrame(data)

def analyze_and_suggest(df):
    summary = df.groupby(["model", "storage", "lock_status"])["price"].agg(["count", "mean", "min", "max"]).sort_values(by="count", ascending=False).head(20)
    summary["suggested_price"] = (summary["mean"] * 0.98).round(2)
    return summary.round(2)

def save_to_file(df, summary):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_path = os.path.join(OUTPUT_DIR, f"raw_data_{timestamp}.csv")
    summary_path = os.path.join(OUTPUT_DIR, f"summary_{timestamp}.csv")

    df.to_csv(full_path, index=False)
    summary.to_csv(summary_path)

    print(f"\n[✔] Raw data saved to {full_path}")
    print(f"[✔] Summary saved to {summary_path}")

def main():
    print("\n[•] Scraping eBay...")
    ebay_data = scrape_ebay("iPhone 13")

    print("[•] Scraping Swappa...")
    swappa_data = scrape_swappa_prices()

    print("[•] Combining data...")
    df = pd.concat([ebay_data, swappa_data], ignore_index=True)
    df = df.dropna(subset=["price"])

    print("[•] Analyzing data...")
    summary = analyze_and_suggest(df)

    print("\n[✔] Top Models Summary:")
    print(summary)

    save_to_file(df, summary)

if __name__ == "__main__":
    main()
