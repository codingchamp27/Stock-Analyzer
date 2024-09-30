import os
import requests
import streamlit as st
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "0.0.0.0")
api_port = 8080

# Streamlit UI elements
st.title("📈 Predict Nifty 50 stocks")
st.markdown(
    """
    ## How to use:
    
    Enter a question about price-action decision for any the Nifty 50 stock or as a whole,
    this app will provide the full analysis of stocks and give output accordingly.

    ---
    """
)

question = st.text_input(
    "Enter your question here (Please mention the stock by ticker symbol) ",
    placeholder="E.g., What will be my price-action decision for TCS.NS stock today? , Find best stocks to buy today.",
)

# Handle the query submission
if question:
    url = f'http://{api_host}:{api_port}/'
    # url = f'http://google.com'
    data = {"query": question}
    headers = {
        "accept": "/",
        "Content-Type": "application/json",
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error(f"Failed to obtain insights. Status code: {response.status_code}")
