# Raw Package
import numpy as np
import pandas as pd
import streamlit as st

# Market Data 
import yfinance as yf

#Graphing/Visualization
from datetime import date
import plotly.graph_objs as go 

#Web Scraping
import requests
from bs4 import BeautifulSoup
import json
import re

def buy_sell_helper(symbol_crypto,crypto_option):
    
    #This is to be sure we'll have internet connection before starting the script
    url = "https://finance.yahoo.com/"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        #If requests is ok, then the next code will work

        if st.sidebar.button("Search"):
            st.title(f"{crypto_option} Buy & Sell Helper")

            ########### Today's Prices Evolution Implementation #############

            # Retrieve stock data frame (df) from yfinance API at an interval of 1m 
            df = yf.download(tickers=symbol_crypto,period='1d',interval='1m')

            ##Actualmente Central European Summer Time (CEST), UTC +2, por lo que en el gráfico aparece como -2 horas (UTC).

            st.subheader(f"Today's {crypto_option} Evolution")

            # Declare plotly figure (go) with only closing prices
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

            st.plotly_chart(fig)



            ########### Simple Moving Average Implementation #############

            data = yf.download(symbol_crypto, start='2010-01-01',
                        end=date.today())
            data = data.reset_index()
            data['Date'] = pd.to_datetime(data['Date'])

           

            data['SMA 20'] = data['Close'].rolling(window=20).mean() #Calculating the latest 20 days mean
            data['SMA 100'] = data['Close'].rolling(window=100).mean() #Calculating the latest 100 days mean

            df.rolling(window=30).mean()
            
            #SMA BUY SELL
            #Function for buy and sell signals
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
            layout = go.Layout(xaxis=dict(title="Date"),yaxis=dict(title="USD") )
            fig = dict(layout=layout,data=data)

            st.plotly_chart(fig)

            ########### Crypto News Implementation #############
            try:
                st.subheader(f"{crypto_option} News")

                symbol_initials = (re.split('-', symbol_crypto))[0]  #Take only the initials from the cryptocoin

                url = 'https://cryptonews-api.com/api/v1?tickers='+ symbol_initials + '&items=50&page=1&token=vkacbvdepnr96rbqmd8e9o95nzl2edjwvbcve3kg'
                html_response = requests.get(url).content
                soup = BeautifulSoup(html_response, "html.parser") 
                site_json=json.loads(soup.text)
                
                news = pd.DataFrame(site_json['data'])

                #Filtering the news by the sentiment

                negative = news['sentiment'].isin(['Negative']).sum(axis=0)
                positive = news['sentiment'].isin(['Positive']).sum(axis=0)
                neutral = news['sentiment'].isin(['Neutral']).sum(axis=0)

                #Showing the sentiments KPIs
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

                
                #Last 30 days Sentiment Analysis Chart
                st.subheader("Last 30 days Sentiment Analysis")

                url2 = 'https://cryptonews-api.com/api/v1/stat?&tickers='+ symbol_initials + '&date=last30days&page=1&token=vkacbvdepnr96rbqmd8e9o95nzl2edjwvbcve3kg'
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


                # Create figure
                fig = go.Figure()

                neutral_articles_plot = go.Scatter(name='Neutral Articles',x=sent_df.Date, y=sent_df.Neutral)
                positive_articles_plot = go.Scatter(name='Positive Articles',x=sent_df.Date, y=sent_df.Positive)
                negative_articles_plot = go.Scatter(name='Negative Articles',x=sent_df.Date, y=sent_df.Negative)

                # Set title
                data = [neutral_articles_plot,negative_articles_plot,positive_articles_plot]
                layout = go.Layout(title ="Articles Sentiment Evolution", xaxis=dict(title="Date"),yaxis=dict(title="Number of News") )
                fig = dict(layout=layout,data=data)
                st.write(fig)

                #Showing the latest 50 news
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
            except:
                pass
            
    #If no internet connection:
    except (requests.ConnectionError, requests.Timeout) as exception:
        st.title("Internet Connection Error.")
        st.markdown("Internet is needed to see Today's Prices evolution.")
