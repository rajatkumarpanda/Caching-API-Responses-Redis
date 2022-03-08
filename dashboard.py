import streamlit as st
import requests
import config
from iex import IEXStock
from helpers import format_number
from datetime import datetime
from json.decoder import JSONDecodeError
from redis import Redis
import json
from datetime import timedelta

redis_client = Redis(host='localhost', port=6379, db=0)

symbol = st.sidebar.text_input("Symbol", value="MSFT")

stock = IEXStock(config.IEX_API_KEY, symbol)


screen = st.sidebar.selectbox("View", 
("Overview","Fundamentals", "News"))

st.title(screen)


if screen == "Overview":
    
    try:
        logo_key = f"{symbol}_logo"
        logo =  redis_client.get(logo_key)

        if logo is None:
            logo = stock.get_logo()
            redis_client.set(f'{symbol}_logo',json.dumps(logo))
        else:
            logo = json.loads(logo)

        company_key = f"{symbol}_desc"
        company_info = redis_client.get(company_key)

        if company_info is None:
            company_info = stock.get_company_info()
            redis_client.set(company_key, json.dumps(company_info))
            redis_client.expire(company_key, timedelta(seconds=30))
        else:
            company_info = json.loads(company_info)
            
        col1, col2 = st.columns([1,4])

        with col1:
            st.image(logo['url'])
        with col2:  
            
            st.subheader(company_info['companyName'])    
            st.subheader('Description')
            st.write(company_info['description'])
            st.subheader('Industry')
            st.write(company_info['industry'])
            st.subheader('CEO')
            st.write(company_info['CEO'])
    except JSONDecodeError as e:
        st.write("Company does not exist.")
    except TypeError as e:
     pass


if screen == "Fundamentals":
    try:
        col1, col2 = st.columns(2)

        with col1:
            stats = stock.get_stats()
            # st.write(stats)
            st.subheader(stats['companyName'])    
            st.subheader('Market Cap')
            st.write(format_number(stats['marketcap']))
            st.subheader('PE Ratio')
            st.write(format_number(stats['peRatio']))
            st.subheader('Week 52 High')
            st.write(stats['week52high'])
            st.subheader('Week 52 Low')
            st.write(stats['week52low'])
        with col2:
            st.subheader('200 Day Moving Average')
            st.write(stats['day200MovingAvg'])
            st.subheader('50 Day Moving Average')
            st.write(stats['day50MovingAvg'])
    except JSONDecodeError as e:
        st.write("Company does not exist.")
    except TypeError as e:
     pass



if screen == "News":
    try:
        news = stock.get_company_news()
        for article in news:
            st.subheader(article['headline'])
            dt = datetime.utcfromtimestamp(article['datetime']/1000).isoformat()
            st.write(f"Posted by {article['source']} at {dt}")
            st.write(article['url'])
            st.write(article['summary'])
            st.image(article['image'])
    except JSONDecodeError as e:
        st.write("Company does not exist.")
    except TypeError as e:
     pass

    
