import pandas as pd
import mplfinance as mpf
import os

# Replace this with your actual file name
csv_file = "D:/Crypto History/labeled_bullish_patterns_20250527_164228.csv"

# Load the labeled dataset
df = pd.read_csv(csv_file)

# Count labels
label_counts = df['label'].value_counts()

# Print summary
print("Label counts:")
print(label_counts)




# === FILE PATHS ===
raw_data_path = "D:/Crypto/Crypto-Tracker-/Crypto/data/solana_history.csv"
labeled_data_path = "D:/Crypto History/labeled_bullish_patterns_20250527_164228.csv"  # Replace with your filename

# === LOAD DATA ===
raw_df = pd.read_csv(raw_data_path)
labeled_df = pd.read_csv(labeled_data_path)

# Add datetime index to raw data for mplfinance
raw_df['timestamp'] = pd.to_datetime(raw_df['timestamp'], unit='ms')
raw_df.set_index('timestamp', inplace=True)

# For tracking examples
output_dir = "D:/Crypto History/validation_charts"
os.makedirs(output_dir, exist_ok=True)

# === SETTINGS ===
max_examples = 10  # Change this to plot more
example_count = 0

# === LOOP OVER LABELED PATTERNS ===
for i in range(3, len(raw_df) - 6):
    if labeled_df.iloc[i - 3]['label'] == 1:
        window = raw_df.iloc[i - 3:i + 3]  # c1, c2, c3 + c4, c5, c6
        if len(window) < 6:
            continue

        timestamp_str = str(window.index[2]).replace(":", "-").replace(" ", "_")
        title = f"Pattern_{example_count+1}_at_{timestamp_str}"
        filename = os.path.join(output_dir, f"{title}.png")


        mpf.plot(
            window,
            type='candle',
            style='charles',
            title=title,
            ylabel='Price',
            savefig=filename
        )

        print(f"✅ Saved: {filename}")
        example_count += 1

        if example_count >= max_examples:
            break
