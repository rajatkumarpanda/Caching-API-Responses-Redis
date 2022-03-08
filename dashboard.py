import streamlit as st
import requests
import config

symbol = st.sidebar.text_input("Symbol", value="MSFT")

screen = st.sidebar.selectbox("View", 
("Overview","Fundamentals", "News", "Ownership", "Technicals"))

st.title(screen)

st.write(symbol)

if screen == "Overview":
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/logo?token={config.IEX_API_KEY}"
    r = requests.get(url)
    response_json = r.json()
    st.image(response_json['url'])


if screen == "Fundamentals":
    pass
if screen == "News":
    pass
if screen == "Ownership":
    pass
if screen == "Technicals":
    pass