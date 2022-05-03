import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.graph_objects as go

#Import local path file 
from dotenv import load_dotenv
import os
load_dotenv()

import sys
sys.path.insert(0,os.getenv('path'))


def crypto_tracker(symbol_crypto,crypto_option):

    crypto_descriptions = pd.read_csv('../data/crypto_descriptions.csv')


    start_date = st.sidebar.date_input("From", date.today() - relativedelta(months=1))
    end_date = st.sidebar.date_input("To", date.today())
    if start_date > end_date:
        st.warning("You seem to have selected a start date greater than end date. Please reselect the dates")

    #symbol_crypto = crypto_mapping[crypto_option]
    data_crypto = yf.Ticker(symbol_crypto)

    value_selector = st.sidebar.selectbox(
        "Value Selector", ("Close", "Open", "High", "Low", "Volume")
    )


    if st.sidebar.button("Search"):
        st.title(f"{crypto_option} Tracker")

        crypto_hist = data_crypto.history(
            start=start_date, end=end_date, interval='1d')

        crypto_hist.index =crypto_hist.index.map(lambda t: t.strftime('%Y-%m-%d'))

        st.subheader("Price Evolution")

        #Calculating max and min closing price (and its date)


        max_closing_price = crypto_hist[value_selector].max()
        max_date = crypto_hist[crypto_hist[value_selector] == max_closing_price].index[0]
        min_closing_price = crypto_hist[value_selector].min()
        min_date = crypto_hist[crypto_hist[value_selector] == min_closing_price].index[0]

        first_kpi, second_kpi = st.columns(2)
        with first_kpi:
            st.markdown(f"**Highest {value_selector} Price for {crypto_option}:**")
            st.markdown(f"<h2 style='text-align: left; color: green;'>{round(max_closing_price,4)} USD</h2>", unsafe_allow_html=True)
            st.markdown(f"Observed on {max_date}")
        with second_kpi:
            st.markdown(f"**Lowest {value_selector} Price for {crypto_option}:**")
            st.markdown(f"<h2 style='text-align: left; color: red;'>{round(min_closing_price,4)} USD</h2>", unsafe_allow_html=True)
            st.markdown(f"Observed on {min_date}")

        #Ploting the timeline evolution of the value selector price
        fig = px.line(crypto_hist, 
        x=crypto_hist.index, y=value_selector,
        labels={"x": "Date"})
        st.plotly_chart(fig)


        st.subheader("Candlestick chart")
        #Calculating max and min differences between Closing and Opening prices
        crypto_hist['Difference'] = crypto_hist.Close - crypto_hist.Open
        max_dif_price = crypto_hist['Difference'].max()
        max_dif_date = crypto_hist[crypto_hist['Difference'] == max_dif_price].index[0]        
        min_dif_price = crypto_hist['Difference'].min()
        min_dif_date = crypto_hist[crypto_hist['Difference'] == min_dif_price].index[0]


        first_kpi_candlestick, second_kpi_first_kpi_candlestick = st.columns(2)
        with first_kpi_candlestick:
            st.markdown(f"**Highest Difference Prices (Closing - Opening) for {crypto_option}:**")
            st.markdown(f"<h2 style='text-align: left; color: green;'>{round(max_dif_price,4)} USD</h2>", unsafe_allow_html=True)
            st.markdown(f"Observed on {max_dif_date}")
        with second_kpi_first_kpi_candlestick:
            st.markdown(f"**Lowest Difference Prices (Closing - Opening) for {crypto_option}:**")
            st.markdown(f"<h2 style='text-align: left; color: red;'>{round(min_dif_price,4)} USD</h2>", unsafe_allow_html=True)
            st.markdown(f"Observed on {min_dif_date}")

        set = { 'x': crypto_hist.index, 'open': crypto_hist.Open, 'close': crypto_hist.Close, 'high': crypto_hist.High, 'low': crypto_hist.Low, 'type': 'candlestick',}
        fig = go.Figure(data=set)
        labels={"x": "Date"}
        st.plotly_chart(fig)


        #Calculating and ploting Daili Cahnge (% comparing previous day)
        st.subheader("Daily Change (%)")
        crypto_hist["Daily Change"] = crypto_hist["Close"].pct_change() * 100
        max_daily_change = crypto_hist["Daily Change"].max()
        max_change_date = crypto_hist[crypto_hist["Daily Change"] == max_daily_change].index[0]        
        min_daily_change = crypto_hist["Daily Change"].min()
        min_change_date = crypto_hist[crypto_hist["Daily Change"] == min_daily_change].index[0]

        first_kpi_change, second_kpi_first_kpi_change = st.columns(2)
        with first_kpi_change:
            st.markdown(f"**Highest Daily Change for {crypto_option}:**")
            st.markdown(f"<h2 style='text-align: left; color: green;'>{round(max_daily_change,2)} %</h2>", unsafe_allow_html=True)
            st.markdown(f"Observed on {max_change_date}")
        with second_kpi_first_kpi_change:
            st.markdown(f"**Lowest Daily Change for {crypto_option}:**")
            st.markdown(f"<h2 style='text-align: left; color: red;'>{round(min_daily_change,2)} USD</h2>", unsafe_allow_html=True)
            st.markdown(f"Observed on {min_change_date}")

        fig = px.line(crypto_hist, 
        x=crypto_hist.index, y="Daily Change",
        labels={"x": "Date"})
        st.plotly_chart(fig)

        description = list(crypto_descriptions[crypto_descriptions['Name']==crypto_option]['Description'])[0]
        st.subheader("Description")
        st.markdown(description)

