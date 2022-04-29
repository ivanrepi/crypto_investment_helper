# Raw Package
import numpy as np
import pandas as pd
import streamlit as st

# Market Data 
import yfinance as yf

#Graphing/Visualization
from datetime import date
import plotly.graph_objs as go 

import matplotlib.pyplot as plt
import plotly.offline as pyo

import requests
from bs4 import BeautifulSoup
import json
import re

def buy_sell_helper():

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
        "Which Crypto do you want to visualize?", list(crypto_mapping.keys()))


    symbol_crypto = crypto_mapping[crypto_option]
    data_crypto = yf.Ticker(symbol_crypto)


    if st.sidebar.button("Search"):
        st.title(f"{crypto_option} Buy & Sell Helper")

        # Retrieve stock data frame (df) from yfinance API at an interval of 1m 
        df = yf.download(tickers=symbol_crypto,period='1d',interval='1m')

        ##Actualmente Central European Summer Time (CEST), UTC +2, por lo que en el gráfico aparece como -2 horas (UTC).

        st.subheader(f"Today's {crypto_option} Evolution")

        # Declare plotly figure (go)
        fig=go.Figure()

        fig.add_trace(go.Scatter(x=df.index,
                        y=df['Close'], name = 'market data'))

        fig.update_layout(
            title= str(symbol_crypto)+' Live Share Price:',
            yaxis_title='Closing Price (USD per Shares)')               

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=3, label="3h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        #fig.show()
        st.plotly_chart(fig)



        data = yf.download(symbol_crypto, start='2010-01-01',
                    end=date.today())
        data = data.reset_index()
        data['Date'] = pd.to_datetime(data['Date'])

        ########### Simple Moving Average Implementation #############

        data['SMA 20'] = data['Close'].rolling(window=20).mean()
        data['SMA 100'] = data['Close'].rolling(window=100).mean()

        df.rolling(window=30).mean()
        #SMA BUY SELL
        #Function for buy and sell signal
        def buy_sell(data):
            signalBuy = []
            signalSell = []
            position = False 

            for i in range(len(data)):
                if data['SMA 20'][i] > data['SMA 100'][i]:
                    if position == False :
                        signalBuy.append(data['Adj Close'][i])
                        signalSell.append(np.nan)
                        position = True
                    else:
                        signalBuy.append(np.nan)
                        signalSell.append(np.nan)
                elif data['SMA 20'][i] < data['SMA 100'][i]:
                    if position == True:
                        signalBuy.append(np.nan)
                        signalSell.append(data['Adj Close'][i])
                        position = False
                    else:
                        signalBuy.append(np.nan)
                        signalSell.append(np.nan)
                else:
                    signalBuy.append(np.nan)
                    signalSell.append(np.nan)
            return pd.Series([signalBuy, signalSell])


        data['Buy_Signal_price'], data['Sell_Signal_price'] = buy_sell(data)


        st.subheader(f"{crypto_option} Price History with buy and sell signals")

        # Create figure
        fig = go.Figure()

        actual_prices_plot = go.Scatter(name=symbol_crypto,x=data.Date, y=data['Adj Close'], line_color='#F1A537')
        sma20_plot = go.Scatter(name='SMA20',x=data.Date, y=data['SMA 20'],line_color="#0000ff")
        sma100_plot = go.Scatter(name='SMA100',x=data.Date, y=data['SMA 100'])
        Buy_Signal_plot = go.Scatter(mode="markers", name='Buy',x=data.Date, y=data['Buy_Signal_price'] , line_color='green', marker_symbol = 'triangle-up', marker_size=10)
        Sell_Signal_plot = go.Scatter(mode="markers", name='Sell',x=data.Date, y=data['Sell_Signal_price'] , line_color='red', marker_symbol = 'triangle-down', marker_size=10)


        # Set title
        fig.update_layout(title= str(symbol_crypto+ " Price History with buy and sell signals"),yaxis_title='Close Price INR (₨)')    

        data = [actual_prices_plot,sma20_plot,sma100_plot,Buy_Signal_plot,Sell_Signal_plot]
        fig = dict(data=data)
        st.plotly_chart(fig)


        st.subheader(f"{crypto_option} News")

        symbol_initials = (re.split('-', symbol_crypto))[0] 

        url = 'https://cryptonews-api.com/api/v1?tickers='+ symbol_initials + '&items=50&page=1&token=u7pvihvex531i03ya2urh3sscf2pcj50k3uxzyu2'
        html_response = requests.get(url).content
        soup = BeautifulSoup(html_response, "html.parser") 
        site_json=json.loads(soup.text)
        
        news = pd.DataFrame(site_json['data'])

        negative = news['sentiment'].isin(['Negative']).sum(axis=0)
        positive = news['sentiment'].isin(['Positive']).sum(axis=0)
        neutral = news['sentiment'].isin(['Neutral']).sum(axis=0)
        
        first_kpi, second_kpi,third_kpi = st.columns(3)
        with first_kpi:
            st.markdown("**Positive Latest News**")
            st.markdown(f"<h2 style='text-align: left; color: green;'>{positive}</h2>", unsafe_allow_html=True)
        with second_kpi:
            st.markdown("**Negative Latest News**")
            st.markdown(f"<h2 style='text-align: left; color: red;'>{negative}</h2>", unsafe_allow_html=True)

        with third_kpi:
            st.markdown("**Neutral Latest News**")
            st.markdown(f"<h2 style='text-align: left; color: black;'>{neutral}</h2>", unsafe_allow_html=True)

        
        st.subheader("Last 30 days Sentiment Analysis")

        url2 = 'https://cryptonews-api.com/api/v1/stat?&tickers='+ symbol_initials + '&date=last30days&page=1&token=u7pvihvex531i03ya2urh3sscf2pcj50k3uxzyu2'
        #url2 = 'https://cryptonews-api.com/api/v1/stat?&tickers=BTC&date=last30days&page=1&token=u7pvihvex531i03ya2urh3sscf2pcj50k3uxzyu2'
        html_response2 = requests.get(url2).content
        soup2 = BeautifulSoup(html_response2, "html.parser") 
        site_json2=json.loads(soup2.text)

        sentiments = pd.DataFrame(site_json2['data'])
        sentiments = sentiments.T


        neutral = []
        positive = []
        negative = []
        i = 0
        while i < len(sentiments):
            neutral.append(sentiments.iloc[i].get(symbol_initials).get('Neutral'))
            positive.append(sentiments.iloc[i].get(symbol_initials).get('Positive'))
            negative.append(sentiments.iloc[i].get(symbol_initials).get('Negative'))
            i+= 1

        sent_df = pd.DataFrame(list(zip(list(sentiments.index),neutral, positive, negative)),
                    columns =['Date','Neutral', 'Positive', 'Negative'])
        sent_df['Date'] = pd.to_datetime(sent_df['Date'])
        #sent_df.plot(x="Date", y=["Neutral", "Positive", "Negative"], kind="line", figsize=(9, 8));


        # Create figure
        fig = go.Figure()

        neutral_articles_plot = go.Scatter(name='Neutral Articles',x=sent_df.Date, y=sent_df.Neutral)
        positive_articles_plot = go.Scatter(name='Positive Articles',x=sent_df.Date, y=sent_df.Positive)
        negative_articles_plot = go.Scatter(name='Negative Articles',x=sent_df.Date, y=sent_df.Negative)

        # Set title
        fig.update_layout(title_text="Articles Sentimen Evolution")

        data = [neutral_articles_plot,negative_articles_plot,positive_articles_plot]
        fig = dict(data=data)
        st.write(fig)




        with st.expander("SEE LATEST NEWS"):
            first_news, second_news, third_news = st.columns(3)
            i = 0
            while i < len(news):
                with first_news:
                    st.image(news['image_url'][i], caption= (news['source_name'][i]) + ' | ' +  (news['date'][i]) )
                    st.markdown(news['title'][i])
                    st.write('[Read the Article]' + '(' + news['news_url'][i] + ')')
                    i += 3
            j = 1
            while j < len(news):
                with second_news:
                    st.image(news['image_url'][j], caption= (news['source_name'][j]) + ' | ' +  (news['date'][j]) )
                    st.markdown(news['title'][j])
                    st.write('[Read the Article]' + '(' + news['news_url'][j] + ')')
                    j+= 3
            k = 2
            while k < len(news):
                with third_news:
                    st.image(news['image_url'][k], caption= (news['source_name'][k]) + ' | ' +  (news['date'][k]) )
                    st.markdown(news['title'][k])
                    st.write('[Read the Article]' + '(' + news['news_url'][k] + ')')
                    k += 3

