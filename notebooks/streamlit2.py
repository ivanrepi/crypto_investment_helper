import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt


df=pd.read_csv('../data/crypto_historical_prices/coin_Bitcoin.csv')
df1=pd.read_csv('../data/crypto_historical_prices/coin_Cardano.csv')



st.title("Share Price analysis for May 2019 to May 2020:")
st.sidebar.title("Share Price analysis for May 2019 to May 2020:")
st.markdown("This application is a Share Price dashboard for Top 5 Gainers and Losers:")
st.sidebar.markdown("This application is a Share Price dashboard for Top 5 Gainers and Losers:")





if st.sidebar.checkbox("Cryptocurrencies Description", False, key='1'):
    st.sidebar.title("Gainers")
    select = st.sidebar.selectbox('Currencies', ['Adani Green Energy', 'GMM Pfaudler', 'AGC Networks', 'Alkyl Amines Chem', 'IOL Chem & Pharma'], key='1')

    st.title("Gainers")
    if select == 'Adani Green Energy':
        for i in ['Low', 'High', 'Close', 'Open']:
            df[i] = df[i].astype('float64')
    #avg_20 = df.Close.rolling(window=20, min_periods=1).mean()
    #avg_50 = df.Close.rolling(window=50, min_periods=1).mean()
    #avg_200 = df.Close.rolling(window=200, min_periods=1).mean()
    set1 = { 'x': df.Date, 'open': df.Open, 'close': df.Close, 'high': df.High, 'low': df.Low, 'type': 'candlestick',}
    #set2 = { 'x': df.Date, 'y': avg_20, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'MA 20 periods'}
    #set3 = { 'x': df.Date, 'y': avg_50, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'yellow' },'name': 'MA 50 periods'}
    #set4 = { 'x': df.Date, 'y': avg_200, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'black' },'name': 'MA 200 periods'}
    #data = [set1, set2, set3, set4]
    fig = go.Figure(data=set1)
    st.plotly_chart(fig)