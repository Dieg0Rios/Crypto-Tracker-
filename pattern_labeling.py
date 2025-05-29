from candle_info import Candle
import pandas as pd

df = pd.read_csv("D:\Crypto\Crypto-Tracker-\Crypto\data\solana_history.csv")

def isbullishengulfing(candle1, candle2):
    if candle1.getopen() > candle1.getclose() and candle2.getopen() < candle2.getclose():
        if candle1.getclose() > candle2.getopen() and candle1.getopen() < candle2.getclose():
            return True
    return False

def isbullishharami(candle1,candle2): 
    if candle1.getopen() >candle1.getclose() and ca

