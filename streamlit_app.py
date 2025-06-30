# app.py
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Load the compressed dataset
df = pd.read_csv("listings.csv")

# Clean price column
df["price"] = df["price"].replace({r"[\$,]": ""}, regex=True).astype(float)

# Config Page
st.set_page_config(page_title="Cambridge Airbnb Dashboard", layout="wide")

# Filters on Sidebar
st.header("Filters")

selected_hood = st.selectbox('Select Neighbourhood', df['neighbourhood_group_cleansed'].unique())

filtered_df = df[df['neighbourhood_group_cleansed'] == selected_hood]

# Dashboard Title
st.title("Cambridge Airbnb Listings Dashboard")

st.image("Cambridge.jpg", width=400)

#Graph Two
st.subheader("Price Distribution")
hist_chart = alt.Chart(filtered).mark_bar(color='#FF7F0E').encode(
    x=alt.X("price:Q", bin=alt.Bin(maxbins=40), title="Price ($)"),
    y=alt.Y("count()", title="Number of Listings")
).properties(width=600)
st.altair_chart(hist_chart, use_container_width=True)
