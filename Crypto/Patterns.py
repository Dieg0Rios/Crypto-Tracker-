import pandas as pd
import os
from datetime import datetime
from tqdm import tqdm

def generate_labeled_bullish_patterns(csv_path, output_dir):
    """
    Reads a CSV of historical candle data and generates labeled 3-candle patterns
    based on whether the next candle confirms a bullish setup.

    Saves the labeled data to a uniquely named file in the output directory.
    """
    print(f"📥 Loading data from: {csv_path}")
    df = pd.read_csv(csv_path)

    # Ensure correct types
    df = df.astype({
        'open': float,
        'high': float,
        'low': float,
        'close': float,
        'volume': float
    })

    print(f"✅ Loaded {len(df)} candles.")

    # Prepare labeled patterns
    patterns = []

    print("🧠 Labeling patterns...")
    for i in tqdm(range(3, len(df) - 1), desc="Labeling", unit="pattern"):
        c1 = df.iloc[i - 3]
        c2 = df.iloc[i - 2]
        c3 = df.iloc[i - 1]
        c4 = df.iloc[i]

        # Helper functions
        def body(c): return abs(c['close'] - c['open'])
        def lower_wick(c): return min(c['open'], c['close']) - c['low']

        # Calculate features
        c1_body = body(c1)
        c2_body = body(c2)
        c3_body = body(c3)
        c3_lower = lower_wick(c3)
        avg_prev_body = (c1_body + c2_body) / 2
        avg_prev_volume = (c1['volume'] + c2['volume']) / 2

        # Label logic (relaxed conditions)
        gain_pct = (c4['close'] - c3['close']) / c3['close']
        is_green = c4['close'] > c4['open']
        broke_high = c4['close'] > c3['high']
        long_lower_wick = c3_lower > 0.1 * c3_body
        strong_body = c3_body > 0.9 * avg_prev_body
        strong_volume = c3['volume'] > 0.9 * avg_prev_volume

        score = sum([
            gain_pct > 0.002,
            is_green,
            broke_high,
            long_lower_wick,
            strong_body,
            strong_volume
        ])

        label = 1 if score >= 4 else 0

        patterns.append({
            'c1_open': c1['open'], 'c1_close': c1['close'],
            'c2_open': c2['open'], 'c2_close': c2['close'],
            'c3_open': c3['open'], 'c3_close': c3['close'],
            'c3_body': c3_body,
            'c3_lower_wick': c3_lower,
            'c3_volume': c3['volume'],
            'c4_close': c4['close'],
            'label': label
        })

    # Save output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"labeled_bullish_patterns_{timestamp}.csv"
    output_path = os.path.join(output_dir, output_filename)

    labeled_df = pd.DataFrame(patterns)
    labeled_df.to_csv(output_path, index=False)

    print(f"✅ Labeled dataset saved to: {output_path}")
    return output_path


# Run the script
if __name__ == "__main__":
    generate_labeled_bullish_patterns(
        "D:/Crypto/Crypto-Tracker-/Crypto/data/solana_history.csv",
        "D:/Crypto History"
    )
