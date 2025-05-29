from candle_info import getopen, gethigh, getlow, getclose 
import pandas as pd

df = pd.read_csv("D:\Crypto\Crypto-Tracker-\Crypto\data\solana_history.csv")

def isbullishengulfing(candle1, candle2):
    if 