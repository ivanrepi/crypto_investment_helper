import yfinance as yf
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.offline as py
import streamlit as st 

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


import plotly.express as px
import plotly.graph_objects as go

import json
from prophet.serialize import model_to_json, model_from_json



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
    st.title(f"{crypto_option} Stock Price Prediction")

    prediction_file_path = '../data/predictions/forecast_'+ symbol_crypto + '.csv'
    model_file_path = '../data/models/serialized_model_'+ symbol_crypto + '.json'

    with open(model_file_path, 'r') as fin:
        model = model_from_json(json.load(fin))  # Load model

    forecast = pd.read_csv(prediction_file_path)
    forecast['ds'] = pd.to_datetime(forecast['ds'])

    fig = plot_plotly(model, forecast) 
    st.write(fig)

    fig2 = model.plot_components(forecast)
    st.write(fig2)


st.sidebar.title("Make your prediction")
st.sidebar.markdown("Select the the  historical data dates for the prediction, as well as the desired number of predicted days:")

start_date = st.sidebar.date_input("Take data from:", date.today() - relativedelta(months=1))
end_date = st.sidebar.date_input("Take data to:", date.today())
    
if start_date > end_date:
    st.warning("You seem to have selected a start date greater than end date. Please reselect the dates")

prediction_days = st.sidebar.number_input(
    "Number of predicted days",
    min_value=1,
    max_value=365)

if st.sidebar.button("Recalculate prediction*"):
    st.title(f"{crypto_option} Stock Price Prediction")
    with st.spinner('Making prediction...'):

        crypto_hist = yf.download(symbol_crypto, start=start_date, end=end_date)
        crypto_hist = crypto_hist.reset_index()
        crypto_hist['Date'] = pd.to_datetime(crypto_hist['Date'])
        crypto_hist[['ds','y']] = crypto_hist[['Date', 'Adj Close']]

        model = Prophet()
        model.fit(crypto_hist)

        future = model.make_future_dataframe(prediction_days, freq='d')
        forecast = model.predict(future)

        fig3 = plot_plotly(model, forecast) 
        st.write(fig3)

        fig4 = model.plot_components(forecast)
        st.write(fig4)
    
st.sidebar.markdown("*This process could take a while")