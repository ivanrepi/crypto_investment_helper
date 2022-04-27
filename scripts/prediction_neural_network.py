import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential
from keras.models import load_model

import joblib
import streamlit as st 

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo


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


crypto_option = st.sidebar.selectbox(
    "Which Crypto price do you want to predict?", list(crypto_mapping.keys()))

symbol_crypto = crypto_mapping[crypto_option]

st.sidebar.title("Stock Price Prediction")
st.sidebar.markdown("Stock price prediction taking into account all historical data:")


if st.sidebar.button("See prediction"):

    st.title(f"{crypto_option} Daily Price Prediction")
    prediction_days = 60
    scaler_filename = "../data/scalers_neural_network/" + symbol_crypto + "_scaler.save"
    model_filename = "../data/models/" + symbol_crypto + "_keras.h5"

    scaler = joblib.load(scaler_filename) 
    model = load_model(model_filename)


    df = yf.download(symbol_crypto, start='2010-01-01',
                end=date.today())
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])

    test_data = yf.download('BTC-USD', start='2020-01-01',
                    end=date.today())
    test_data = test_data.reset_index()
    actual_prices = test_data['Close'].values

    total_dataset = pd.concat((df['Close'], test_data['Close']), axis=0)

    model_inputs = total_dataset[len(total_dataset)-len(test_data)- prediction_days:].values
    model_inputs = model_inputs.reshape(-1,1)
    model_inputs = scaler.fit_transform(model_inputs)

    x_test = []
    for x in range (prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x-prediction_days:x,0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1],1))

    prediction_prices = model.predict(x_test)
    prediction_prices = scaler.inverse_transform(prediction_prices)


    #Creating results dataframe and saving them as a CSV file
    df1 = pd.DataFrame(test_data.Date)
    df1['prediction_prices'] = prediction_prices
    df1['actual_prices'] = actual_prices

    #Predict Next Day
    real_data = [model_inputs[len(model_inputs) - prediction_days:len(model_inputs) +1 , 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)

    st.subheader('Short Term Prediction (Neural Network Prediction)')
    #Showing tomorrow's price prediction as a KPI:
    first_kpi, second_kpi = st.columns(2)
    with first_kpi:
        st.markdown("**Tomorrow's Closing Price Prediction (USD):**")
        st.markdown(f"<h2 style='text-align: left; color: red;'>{prediction[0][0]}</h2>", unsafe_allow_html=True)

    # Create figure
    fig = go.Figure()

    actual_prices_plot = go.Scatter(name='Actual prices',x=df1.Date, y=df1.actual_prices)
    prediction_prices_plot = go.Scatter(name='Predicted prices',x=df1.Date, y=df1.prediction_prices)

    # Set title
    fig.update_layout(title_text="Bitcoin price prediction")

    data = [actual_prices_plot,prediction_prices_plot]
    fig = dict(data=data)
    st.write(fig)



    

    