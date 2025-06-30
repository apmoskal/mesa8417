import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import pydeck as pdk

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
unique_hoods.insert(0, "All")  # Add "All" at the top
selected_hood = st.sidebar.selectbox('Select Neighbourhood', unique_hoods)

if selected_hood == "All":
    filtered_df = df
else:
    filtered_df = df[df['neighbourhood_cleansed'] == selected_hood]

# Dashboard Title
st.title("Cambridge Airbnb Listings Dashboard")

st.image("Cambridge.jpg", width=400)

st.subheader("Map of Listings")

# Prepare data for map (remove rows with missing coordinates)
map_df = filtered_df.dropna(subset=['latitude', 'longitude'])

if not map_df.empty:
    st.map(map_df[['latitude', 'longitude']])
else:
    st.info("No listings available for this neighbourhood.")

# Graph Two
st.subheader("Price Distribution")
hist_chart = alt.Chart(filtered_df).mark_bar(color='#FF7F0E').encode(
    x=alt.X("price:Q", bin=alt.Bin(maxbins=40), title="Price ($)"),
    y=alt.Y("count()", title="Number of Listings")
).properties(width=600)
st.altair_chart(hist_chart, use_container_width=True)
