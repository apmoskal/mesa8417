import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Load the compressed dataset
df = pd.read_csv("listings.csv")

# Clean data
df["price"] = df["price"].replace({r"[\$,]": ""}, regex=True).astype(float)

#Fill NaN with a default value
df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].fillna('Not Listed')
df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].astype(str).str.strip()

# Config Page
st.set_page_config(page_title="Cambridge Airbnb Dashboard", layout="wide")

# Filters on Sidebar
st.sidebar.header("Filters")  # Move filters to the sidebar

# Show dropdown with all unique neighbourhoods
unique_hoods = sorted([hood for hood in df['neighbourhood_cleansed'].unique() if hood and hood != 'nan'])
selected_hood = st.sidebar.selectbox('Select Neighbourhood', unique_hoods)

filtered_df = df[df['neighbourhood_cleansed'] == selected_hood]

# Dashboard Title
st.title("Cambridge Airbnb Listings Dashboard")

st.image("Cambridge.jpg", width=400)

# Graph Two
st.subheader("Price Distribution")
hist_chart = alt.Chart(filtered_df).mark_bar(color='#FF7F0E').encode(
    x=alt.X("price:Q", bin=alt.Bin(maxbins=40), title="Price ($)"),
    y=alt.Y("count()", title="Number of Listings")
).properties(width=600)
st.altair_chart(hist_chart, use_container_width=True)
