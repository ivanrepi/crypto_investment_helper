from operator import ne
from turtle import title
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt


cryptos_list= ['Aave','BinanceCoin','Bitcoin','Cardano','ChainLink','Cosmos','CryptocomCoin','Dogecoin','EOS','Ethereum','Iota','Litecoin','Monero','NEM','Polkadot','Solana','Stellar','Tether','Tron','Uniswap','USDCoin','WrappedBitcoin','XRP']
options_list = ['Cryptocurrencies Description', 'Price Prediction', 'Buy & Sell']


aave = pd.read_csv('../data/crypto_historical_prices/coin_Aave.csv')
binance_coin = pd.read_csv('../data/crypto_historical_prices/coin_BinanceCoin.csv')
bitcoin = pd.read_csv('../data/crypto_historical_prices/coin_Bitcoin.csv')
cardano = pd.read_csv('../data/crypto_historical_prices/coin_Cardano.csv')
chain_link = pd.read_csv('../data/crypto_historical_prices/coin_ChainLink.csv')
cosmos = pd.read_csv('../data/crypto_historical_prices/coin_Cosmos.csv')
cryptocom_coin = pd.read_csv('../data/crypto_historical_prices/coin_CryptocomCoin.csv')
dogecoin = pd.read_csv('../data/crypto_historical_prices/coin_Dogecoin.csv')
eos = pd.read_csv('../data/crypto_historical_prices/coin_EOS.csv')
ethereum = pd.read_csv('../data/crypto_historical_prices/coin_Ethereum.csv')
iota = pd.read_csv('../data/crypto_historical_prices/coin_Iota.csv')
litecoin = pd.read_csv('../data/crypto_historical_prices/coin_Litecoin.csv')
monero = pd.read_csv('../data/crypto_historical_prices/coin_Monero.csv')
nem = pd.read_csv('../data/crypto_historical_prices/coin_NEM.csv')
polkadot = pd.read_csv('../data/crypto_historical_prices/coin_Polkadot.csv')
solana = pd.read_csv('../data/crypto_historical_prices/coin_Solana.csv')
stellar = pd.read_csv('../data/crypto_historical_prices/coin_Stellar.csv')
tether = pd.read_csv('../data/crypto_historical_prices/coin_Tether.csv')
tron = pd.read_csv('../data/crypto_historical_prices/coin_Tron.csv')
uniswap = pd.read_csv('../data/crypto_historical_prices/coin_Uniswap.csv')
usd_coin = pd.read_csv('../data/crypto_historical_prices/coin_USDCoin.csv')
wrapped_bitcoin = pd.read_csv('../data/crypto_historical_prices/coin_WrappedBitcoin.csv')
xrp = pd.read_csv('../data/crypto_historical_prices/coin_XRP.csv')



st.title("Share Price analysis for May 2019 to May 2020:")
st.sidebar.title("Share Price analysis for May 2019 to May 2020:")
st.markdown("This application is a Share Price dashboard for Top 5 Gainers and Losers:")
st.sidebar.markdown("This application is a Share Price dashboard for Top 5 Gainers and Losers:")

select = st.sidebar.selectbox("Select an Option:", options_list, key='1')



if select =='Cryptocurrencies Description':

    #st.sidebar.subheader("Top Cryptocurrencies")
    selection = st.sidebar.selectbox('Most Popular Cryptocurrencies', cryptos_list, key='1')

    st.title("Historical Data")
    if selection == 'Aave':
        df = aave
    elif selection == 'BinanceCoin':
        df = binance_coin
    elif selection == 'Bitcoin':
        df = bitcoin
    elif selection == 'Cardano':
        df = cardano
    elif selection == 'ChainLink':
        df = chain_link
    elif selection == 'Cosmos':
        df = cosmos
    elif selection == 'CryptocomCoin':
        df = cryptocom_coin
    elif selection == 'Dogecoin':
        df = dogecoin
    elif selection == 'EOS':
        df = eos
    elif selection == 'Ethereum':
        df = ethereum
    elif selection == 'Iota':
        df = iota
    elif selection == 'Litecoin':
        df = litecoin
    elif selection == 'Monero':
        df = monero
    elif selection == 'NEM':
        df = nem
    elif selection == 'Polkadot':
        df = polkadot
    elif selection == 'Solana':
        df = solana
    elif selection == 'Stellar':
        df = stellar
    elif selection == 'Tether':
        df = tether
    elif selection == 'Tron':
        df = tron
    elif selection == 'Uniswap':
        df = uniswap
    elif selection == 'USDCoin':
        df = usd_coin
    elif selection == 'WrappedBitcoin':
        df = wrapped_bitcoin
    elif selection == 'XRP':
        df = xrp


    set1 = { 'x': df.Date, 'y': df.Close, 'type': 'bar',}
    set2 = { 'x': df.Date, 'open': df.Open, 'close': df.Close, 'high': df.High, 'low': df.Low, 'type': 'candlestick',}

    #set2 = { 'x': df.Date, 'y': avg_20, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'MA 20 periods'}
    #set3 = { 'x': df.Date, 'y': avg_50, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'yellow' },'name': 'MA 50 periods'}
    #set4 = { 'x': df.Date, 'y': avg_200, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'black' },'name': 'MA 200 periods'}
    #data = [set1, set2, set3, set4]
    fig = go.Figure(data=set1)
    fig2 = go.Figure(data=set2)
    st.subheader("Close Price Evolution")
    st.plotly_chart(fig)
    st.subheader("Candlestick chart")
    st.plotly_chart(fig2)


    st.sidebar.subheader("Cryptos Comparison")
    selection = st.sidebar.multiselect('Select two or more types:', cryptos_list)
    #set1 = { 'x': df.Date, 'open': df.Open, 'close': df.Close, 'high': df.High, 'low': df.Low, 'type': 'candlestick',}
    #set2 = { 'x': df.Date, 'y': avg_20, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'MA 20 periods'}
    #set3 = { 'x': df.Date, 'y': avg_50, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'yellow' },'name': 'MA 50 periods'}
    #set4 = { 'x': df.Date, 'y': avg_200, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'black' },'name': 'MA 200 periods'}
    #data = [set1, set2, set3, set4]
    #fig = go.Figure(data=data)
    #st.plotly_chart(fig)