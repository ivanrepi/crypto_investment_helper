import streamlit as st
import sys
from streamlit import cli as stcli
import pandas as pd

from scripts import crypto_tracker as ct
from scripts import crypto_predictor as cp
from scripts import buy_sell_helper as bsh



def main():
    def set_bg_hack_url():
            
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url("https://wallpaperaccess.com/full/1205123.jpg");
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    st.set_page_config(
        page_title="CryptoAnalysis",
        page_icon="🧊",

        menu_items={
            "Get Help": "https://github.com/ivanrepi",
            "Report a bug": "https://github.com/ivanrepi",
            "About": "# This app serves is an MVP for interactive dashboards that can be used for financial data analysis",
        },
    )
    set_bg_hack_url()

    st.title("Cryptocurrencies Investment Helper")
    
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


    options_list = ['Cryptocurrencies Analysis', 'Price Prediction', 'Buy & Sell']

    st.sidebar.title("Market Helper")
    st.sidebar.markdown("This app will help you on data analysis, price prediction and other helpful tools for the investment decisions")
    select = st.sidebar.selectbox("Select an Option:", options_list, key='1')

    crypto_option = st.sidebar.selectbox(
        "Which Crypto do you want to visualize?", list(crypto_mapping.keys()))
    symbol_crypto = crypto_mapping[crypto_option]


    if select =='Cryptocurrencies Analysis':
        ct.crypto_tracker(symbol_crypto,crypto_option)

    if select =='Price Prediction':
        cp.crypto_predictor(symbol_crypto,crypto_option)

    if select == 'Buy & Sell':
        bsh.buy_sell_helper(symbol_crypto,crypto_option)

if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

