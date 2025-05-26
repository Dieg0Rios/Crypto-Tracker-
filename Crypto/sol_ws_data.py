import websocket
import json
import csv
import os

candle_count = 0

# Ensure data folder exists
if not os.path.exists('data'):
    os.makedirs('data')

# Write header once before starting
with open('data/solana_candles.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])

def on_message(ws, message):
    global candle_count
    data = json.loads(message)
    candle = data['k']  # candle data key

    if candle['x']:  # candle closed
        candle_count += 1

        timestamp = candle['t']
        open_price = candle['o']
        high_price = candle['h']
        low_price = candle['l']
        close_price = candle['c']
        volume = candle['v']

        with open('data/solana_candles.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, open_price, high_price, low_price, close_price, volume])

        print(f"Candle {candle_count} closed and saved at {timestamp}")

        if candle_count >= 10:
            print("10 candles received, closing WebSocket.")
            ws.close()

def on_open(ws):
    print("WebSocket connection opened.")
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": ["solusdt@kline_1m"],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed.")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/solusdt@kline_1m",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()
