import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
from prophet import Prophet
import json
from prophet.serialize import model_to_json
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential
from keras.models import load_model

import joblib


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
    historical_data_path = 'data/historical_yfinance/'+ symbol_crypto + '.csv'
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

    prediction_file_path = 'data/predictions/forecast_'+ symbol_crypto + '.csv'
    model_file_path = 'data/models/serialized_model_'+ symbol_crypto + '.json'
    with open(model_file_path, 'w') as fout:
        json.dump(model_to_json(model), fout) 

    #Save the prediction
    forecast.to_csv(prediction_file_path)

    return (f'{symbol_crypto} Model and Prediction saved properly')


prediction_days = 60 #Number of past days to take into account to calculate the prediction

def save_neural_network(symbol_crypto):


    df = yf.download(symbol_crypto, start='2010-01-01',
                    end=date.today())
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])


    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1,1))


    x_train, y_train = [], []
    for x in range (prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1],1))


    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50)) 
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=25, batch_size=32)

    #Save Scaler and Model
    scaler_filename = "data/scalers_neural_network/" + symbol_crypto + "_scaler.save"
    model_filename = "data/models/" + symbol_crypto + "_keras.h5"

    joblib.dump(scaler, scaler_filename) 
    model.save(model_filename)

    return (f'{symbol_crypto} Model and scaler (Neural Network) saved properly')


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
    save_neural_network(symbol_crypto)
