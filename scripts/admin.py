import yfinance as yf
import pandas as pd
from datetime import date
from prophet import Prophet
import json
from prophet.serialize import model_to_json


crypto_mapping = {"Bitcoin": "BTC-USD", 
                "Ethereum": "ETH-USD", 
                "Tether": "USDT-USD", 
                "BNB": "BNB-USD", 
                "USD Coin": "USDC-USD", 
                "Solana": "SOL-USD", 
                "XRP": "XRP-USD", 
                "Terra": "LUNA-USD", 
                "Cardano": "ADA-USD", 
                "Avalanche": "AVAX-USD", 
                "Dogecoin": "DOGE-USD", 
                "TerraUSD": "UST-USD", 
                "Binance USD": "BUSD-USD", 
                "Shiba Inu": "SHIB-USD",
                "Wrapped Bitcoin": "WBTC-USD"}

#This function will save all historical data from crypto beggining to current uploaded day
def save_historical_data(symbol_crypto):
    historical_data_path = '../data/historical_yfinance/'+ symbol_crypto + '.csv'
    return df.to_csv(historical_data_path)

#This function calculates and save prophet prediction as well as its model
def save_prophet(symbol_crypto):
    prediction_days = 365
    df[['ds','y']] = df [['Date', 'Adj Close']]
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(prediction_days, freq='d')
    forecast = model.predict(future)

    #Save the model 

    prediction_file_path = '../data/predictions/forecast_'+ symbol_crypto + '.csv'
    model_file_path = '../data/models/serialized_model_'+ symbol_crypto + '.json'
    with open(model_file_path, 'w') as fout:
        json.dump(model_to_json(model), fout) 

    #Save the prediction
    forecast.to_csv(prediction_file_path)

    return (f'{symbol_crypto} Model and Prediction save properly')


#Getting and applying functions to all listed cryptocurrencies               
for i in crypto_mapping:
    print (crypto_mapping[i])
    symbol_crypto = crypto_mapping[i]

    df = yf.download(symbol_crypto, start='2010-01-01',
                end=date.today())
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])

    save_historical_data(symbol_crypto)
    save_prophet(symbol_crypto)
