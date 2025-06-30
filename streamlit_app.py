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

neighborhoods = ["All"] + sorted(df["neighbourhood_group_cleansed"].dropna().unique().tolist())
selected_neigh = st.selectbox("Neighbourhood", neighborhoods)

price_min = int(df["price"].min())
price_max = int(df["price"].max())
selected_price = st.slider("Price Range", min_value=price_min, max_value=price_max, value=(50, 500))

# Filter Data
filtered = df.copy()
if selected_neigh != "All":
    filtered = filtered[filtered["neighbourhood_group_cleansed"] == selected_neigh]
filtered = filtered[filtered["price"].between(*selected_price)]

# Dashboard Title
st.title("Cambridge Airbnb Listings Dashboard")

st.image("Cambridge.jpg", width=400)

#Graph One
st.subheader("Average Price by Room Type")
avg_price = filtered.groupby("room_type")["price"].mean().reset_index()
bar_chart = alt.Chart(avg_price).mark_bar().encode(
    x=alt.X("room_type:N", title="Room Type"),
    y=alt.Y("price:Q", title="Average Price ($)"),
    tooltip=["room_type", "price"]
).properties(width=600)
st.altair_chart(bar_chart, use_container_width=True)

#Graph Two
st.subheader("Price Distribution")
hist_chart = alt.Chart(filtered).mark_bar(color='#FF7F0E').encode(
    x=alt.X("price:Q", bin=alt.Bin(maxbins=40), title="Price ($)"),
    y=alt.Y("count()", title="Number of Listings")
).properties(width=600)
st.altair_chart(hist_chart, use_container_width=True)

#Graph Three
st.subheader("Filtered Listings")
st.dataframe(filtered)

##Graph Four
bar_chart = alt.Chart(filtered).mark_bar().encode(
    x=alt.X('neighbourhood_cleansed').sort('-y'),
    y=alt.Y('count()', title='Available Property Count'),
    color=alt.condition('filtered', 'neighbourhood_cleansed', alt.value('lightgray'), legend=None),
    tooltip=['neighbourhood_cleansed', 'count()']
)
