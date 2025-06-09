# 📱 EZ Mobile Pricing Tool

A Python script that scrapes real-time listings for iPhone 13 models from eBay and Swappa, analyzes prices by model, storage, and lock status, and suggests optimal resale prices.

---

## Features

- Scrapes **eBay** and **Swappa** for real-time phone listings
- Classifies listings by:
  - Model (13, 13 Mini, 13 Pro, Pro Max)
  - Storage (128GB, 256GB, 512GB)
  - Lock Status (Unlocked, Locked)
- Filters out irrelevant or misleading listings
- Calculates and suggests resale prices
- Saves raw data and summary reports as `.csv`

---

## Example Output

```bash
[✔] Raw data saved to pricing_output/raw_data_20250609_121858.csv
[✔] Summary saved to pricing_output/summary_20250609_121858.csv
```

### Sample Summary Output:

| model             | storage | lock_status | count | mean  | min   | max   | suggested_price |
| ----------------- | ------- | ----------- | ----- | ----- | ----- | ----- | --------------- |
| iPhone 13 Pro Max | 256GB   | unlocked    | 12    | 589.0 | 550.0 | 620.0 | 577.22          |
| iPhone 13         | 128GB   | locked      | 8     | 345.5 | 300.0 | 375.0 | 338.59          |

---

## 🛠 Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`
- `pandas`

Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests beautifulsoup4 pandas
```

---

## Output

All output files are saved in the `pricing_output/` folder:

- `raw_data_<timestamp>.csv`: All listings scraped
- `summary_<timestamp>.csv`: Aggregated summary with price suggestions

---
