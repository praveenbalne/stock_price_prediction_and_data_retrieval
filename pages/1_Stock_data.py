#Importing Required Packages

import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime


# Page title
st.markdown('''
# Stock Price Data
Shown are the stock price data for query companies!

''')
st.write('---')


# Subheader
st.subheader('Query parameters')
start_date = st.date_input("Start date", datetime.date(2021, 1, 1))
end_date = st.date_input("End date", datetime.date(2022, 1, 31))


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
    
    return ticker_list

List_of_Companies = get_data() # Companies List


# Removing Company Name and retreiving only the stock code
tickerSymbol = st.selectbox('Stock Picker', List_of_Companies) # Select ticker symbol
i = tickerSymbol.index('(')
tickerSymbol = tickerSymbol[:i]


# Loading Ticker Information
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker


# Ticker information
string_logo = '<img src=%s>' % tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)


# Displaying the Companies Name As Business Summary Heading
string_name = tickerData.info['longName']
st.header('**%s**' % string_name)


# Getting the Business Summary Of the Company to Display
string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)


# Ticker data
st.header('**Picked Stock data**')
st.write(tickerDf)


# Displaying the Graph stock inforamtion using cufflinks
# Bollinger bands
st.header('**Stock Price Graph**')
qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

