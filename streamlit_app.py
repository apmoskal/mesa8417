import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import pydeck as pdk

# Load the compressed dataset
df = pd.read_csv("listings.csv")

# Clean data
df["price"] = df["price"].replace({r"[\$,]": ""}, regex=True).astype(float)

bins = [0, 1, 2, 3, 4, 5]
labels = ['(0-1]', '(1-2]', '(2-3]', '(3-4]', '(4-5]']
df['rating_bin'] = pd.cut(df['review_scores_rating'], bins=bins, labels=labels, include_lowest=True, right=True)

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
st.title("Cambridge 🚣 Airbnb Listings Dashboard")

st.image("Cambridge.jpg", use_container_width=True)

st.subheader("Map of Listings")

# Graph One
# Prepare data for map (remove rows with missing coordinates)
map_df = filtered_df.dropna(subset=['latitude', 'longitude'])

if not map_df.empty:
    st.map(map_df[['latitude', 'longitude']])
else:
    st.info("No listings available for this neighbourhood.")

# Graph Two
st.subheader(f"Price Distribution in {selected_hood}")
hist_chart = alt.Chart(filtered_df).mark_bar(color='#FF7F0E').encode(
    x=alt.X("price:Q", bin=alt.Bin(maxbins=40), title="Price ($)"),
    y=alt.Y("count()", title="Number of Listings")
).properties(width=600)
st.altair_chart(hist_chart, use_container_width=True)


# Graph Three
st.subheader(f"Boxplot of Price by Review Scores Rating ({selected_hood})")
box_chart = alt.Chart(filtered_df.dropna(subset=['rating_bin', 'price'])).mark_boxplot(extent='min-max').encode(
    x=alt.X('rating_bin:N', title='Review Scores Rating Bin'),
    y=alt.Y('price:Q', title='Price ($)'),
    color=alt.Color('rating_bin:N', legend=None)
).properties(width=600)

st.altair_chart(box_chart, use_container_width=True)
