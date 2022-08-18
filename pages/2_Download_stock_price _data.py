# Importing Required Packages

import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime


# Page title
st.markdown('''
# Download Stock Price Data
Shown are the stock price data for query companies!

''')
st.write('---')


# Subheader
st.subheader('Query parameters')
start_date = st.date_input("Start date", datetime.date(2021, 1, 1))
end_date = st.date_input("End date", datetime.date(2022, 1, 31))


# Loading Companies List to Select
@st.cache
def get_data():
    # Retrieving tickers data
    path = 'stock_codes_names.txt'
    file = open( path ,'r')
    lines = file.readlines()
    ticker_list = []

    for line in lines:
        ticker_list.append(line)
    
    return ticker_list

List_of_Companies = get_data()


# Removing Company Name and retreiving only the stock code
tickerSymbol = st.selectbox('Stock Picker', List_of_Companies) # Select ticker symbol
i = tickerSymbol.index('(')
tickerSymbol = tickerSymbol[:i]


# Loading Ticker DataSet
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker
st.write()


# Picked Stock information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)


# Picked Stock data
st.header('**Picked Stock data**')
st.write(tickerDf)


# Providing the Download Button to Download The Selected Stock price data in .csv file format
st.download_button(
    label="Download CSV file",
    data=tickerDf.to_csv(),
    file_name="stock data.csv",
    mime='text/csv',
    )
