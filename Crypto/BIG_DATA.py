import requests
import time
import csv
import os
from tqdm import tqdm  # for progress bar

# Settings
symbol = "SOLUSDT"
interval = "1m"
limit = 1000
output_file = "data/solana_history.csv"

# Create folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Start date (if no CSV exists)
start_time = int(time.mktime(time.strptime('2021-01-01', '%Y-%m-%d'))) * 1000

# If file exists, get the last saved timestamp
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        lines = f.readlines()
        if len(lines) > 1:
            last_line = lines[-1].strip().split(",")
            start_time = int(last_line[0]) + 60_000  # next minute

# Write header if file is empty
write_header = not os.path.exists(output_file) or os.stat(output_file).st_size == 0

# Estimate number of total candles to download (optional, for progress bar)
now = int(time.time() * 1000)
estimated_total = (now - start_time) // 60_000  # number of 1-minute intervals

print(f"Starting download from {time.strftime('%Y-%m-%d %H:%M', time.gmtime(start_time/1000))}")
print(f"Estimated candles to fetch: {estimated_total:,}")

with open(output_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if write_header:
        writer.writerow(['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    with tqdm(total=estimated_total, unit="candle") as pbar:
        while True:
            url = "https://api.binance.com/api/v3/klines"
            params = {
                "symbol": symbol,
                "interval": interval,
                "startTime": start_time,
                "limit": limit
            }

            try:
                response = requests.get(url, params=params)
                data = response.json()
            except Exception as e:
                print("Error fetching data:", e)
                time.sleep(5)
                continue

            if not data:
                print("No more data available.")
                break

            for candle in data:
                writer.writerow([
                    candle[0], candle[1], candle[2],
                    candle[3], candle[4], candle[5]
                ])
                pbar.update(1)

            start_time = data[-1][0] + 60_000  # move to next minute
            time.sleep(0.5)  # avoid rate limit
