# Importing the Required Packages

import streamlit as st
from datetime import date

import yfinance as yf
from prophet.forecaster import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd


# Home Page Title
st.title("Stock Prediction Dashboard")
st.write("###")


# Loading the Companies List to select
@st.cache
def get_data():
    # Retrieving tickers data
    path = 'stock_codes_names.txt'
    file = open( path ,'r')
    lines = file.readlines()
    ticker_list = []

    for line in lines:
        ticker_list.append(line)
    
    file.close()
    return ticker_list

List_of_Companies = get_data() # Companies List

START = "2015-01-01" # Fixing the default Start date for Dataset
TODAY = date.today().strftime("%Y-%m-%d") # Fixing the End date as present day


# Selecting the Company from Select Box List to  Load the Dataset for the model
tickerSymbol = st.selectbox('Select Company to Predict Stock Price for Future Span', List_of_Companies) # Select ticker symbol
i = tickerSymbol.index('(')
tickerSymbol = tickerSymbol[:i]


# Slider to Select the span of prediction (minimum 1 to maximum 5)
n_years = st.slider("", 1, 5)
period = n_years * 365


# Loading the Dataset for the Selected Company to Train and Test the Model
@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


# Loading the Datset
data_load_state = st.text("Load data ...")
data = load_data(tickerSymbol)
data_load_state.text("Loading data ... Done!")

st.write("###")


# Displaying the tail of the dataset as Raw Data
st.subheader("Raw data")
st.write(data.tail())


# Ploting Raw DataSet Graph for the selected company
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text = "Time Series Data", xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

plot_raw_data()


# Forecasting The future Price for selected span
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)

future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.write("***")
st.write("###")


# Displaying the forcated Data
st.subheader("Forecast data")
st.write(forecast.tail())


# Displaying The forecated Price Graph
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)


# Displaying the Yearly, Manthly, Weekly Trend Analysis
st.subheader("Forecast Components")
fig2 = m.plot_components(forecast)
st.write(fig2)
