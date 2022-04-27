from operator import ne
from turtle import title
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import crypto_tracker as ct
import crypto_predictor as cp


st.set_page_config(
    page_title="CryptoAnalysis",
    page_icon="🧊",
    #layout="wide",
    #initial_sidebar_state="auto",
    menu_items={
        "Get Help": "https://github.com/ivanrepi",
        "Report a bug": "https://github.com/ivanrepi",
        "About": "# This app serves is an MVP for interactive dashboards that can be used for financial data analysis",
    },
)

st.title("Cryptocurrencies Investment Helper")
#st.subheader("Ivan Repilado - Ironhack")
#st.markdown("This application takes into account the Top Cryptocurrencies in the market")


options_list = ['Cryptocurrencies Analysis', 'Price Prediction', 'Buy & Sell']

st.sidebar.title("Market Helper")
st.sidebar.markdown("This app will help you on data analysis, price prediction and other helpful tools for the investment decisions")
select = st.sidebar.selectbox("Select an Option:", options_list, key='1')



if select =='Cryptocurrencies Analysis':
    ct.crypto_tracker()

if select =='Price Prediction':
    cp.crypto_predictor()

    #st.sidebar.subheader("Cryptos Comparison")
    #selection = st.sidebar.multiselect('Select two or more types:', cryptos_list)
    #set1 = { 'x': df.Date, 'open': df.Open, 'close': df.Close, 'high': df.High, 'low': df.Low, 'type': 'candlestick',}
    #set2 = { 'x': df.Date, 'y': avg_20, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'MA 20 periods'}
    #set3 = { 'x': df.Date, 'y': avg_50, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'yellow' },'name': 'MA 50 periods'}
    #set4 = { 'x': df.Date, 'y': avg_200, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'black' },'name': 'MA 200 periods'}
    #data = [set1, set2, set3, set4]
    #fig = go.Figure(data=data)
    #st.plotly_chart(fig)