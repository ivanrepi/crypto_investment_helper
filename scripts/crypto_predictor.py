import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
import streamlit as st 

from datetime import date
from dateutil.relativedelta import relativedelta

from keras.models import load_model
import joblib

import plotly.express as px
import plotly.graph_objects as go

import json
from prophet.serialize import model_from_json

def crypto_predictor(symbol_crypto,crypto_option):

    st.sidebar.title("Stock Price Prediction")
    st.sidebar.markdown("Stock price prediction taking into account all historical data:")


    if st.sidebar.button("See prediction"):
        st.title(f"{crypto_option} Stock Price Prediction")
        with st.spinner('Looking to the future...'):

            #Short Term Prediction (Neural Network Prediction)
            prediction_days = 60
            scaler_filename = "../data/scalers_neural_network/" + symbol_crypto + "_scaler.save"
            model_filename = "../data/models/" + symbol_crypto + "_keras.h5"

            scaler = joblib.load(scaler_filename) 
            model = load_model(model_filename)


            df = yf.download(symbol_crypto, start='2010-01-01',
                        end=date.today())
            df = df.reset_index()
            df['Date'] = pd.to_datetime(df['Date'])

            test_data = yf.download('BTC-USD', start=date.today() - relativedelta(months=14),
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


            #Creating results dataframe
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






            #Long Term Prediction (FBProphet Prediction)
            st.subheader('Long Term Prediction (FBProphet Prediction)')
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
        st.title(f"{crypto_option} Customized Prediction")
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