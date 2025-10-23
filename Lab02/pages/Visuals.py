# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import requests
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

#st.info("TODO: Add your data loading logic here.")


# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")
st.divider()
# GRAPH 1: STATIC GRAPH
st.subheader("Static: Film Ratings Histogram")
try:
    df = pd.read_csv("data.csv")
    st.bar_chart(df.set_index("Film")) #NEW
except FileNotFoundError:
    st.write("Add a rating to get started!!")

"""
This graph displays the ratings given in the survey page as a bar chart. 
"""
# GRAPH 2: DYNAMIC GRAPH
"""
This graph lets the user choose which decades to display with my scores for films per decade.
"""
st.divider()
st.subheader("Dynamic: My average ratings per decade.") 
jsonurl = "https://raw.githubusercontent.com/lhernstberger/cs1301lab2/refs/heads/main/Lab02/data.json"

response = requests.get(jsonurl)
my_data = response.json()
dmy = pd.DataFrame(my_data["my_data"])

if "decades" not in st.session_state: #NEW
    st.session_state.decades= (
        int(dmy["Decade"].min()),
        int(dmy["Decade"].max())
    )

min_decade, max_decade = st.slider( #NEW
    "Choose decades to display",
    min_value=int(dmy["Decade"].min()),
    max_value=int(dmy["Decade"].max()),
    value=st.session_state.decades,
    step=10)
st.session_state.decades=(min_decade,max_decade)
filtered_df = dmy[(dmy["Decade"] >= min_decade) & (dmy["Decade"] <= max_decade)]
st.line_chart(filtered_df.set_index("Decade")["MyAverage"]) #NEW
"""
This graph lets the user sort by my average rating per decade, getting to pick which decade.
"""
# GRAPH 3: DYNAMIC GRAPH
jsonurl2 = "https://raw.githubusercontent.com/lhernstberger/cs1301lab2full/refs/main/Lab02/ratings.csv"
response = requests.get(jsonurl2)
my_data = response.json()
st.divider()
st.subheader("Dynamic: My Letterboxd Ratings by score and year")
#df2 = pd.read_csv("ratings.csv")
if "years" not in st.session_state:
    st.session_state.years = (int(df2["Year"].min()), int(df2["Year"].max()))
if "scores" not in st.session_state:
    st.session_state.scores = (float(df2["Rating"].min()), float(df2["Rating"].max()))
yearmin, yearmax = st.slider(
    "Select year range",
    min_value=int(df2["Year"].min()),
    max_value=int(df2["Year"].max()),
    value=st.session_state.years,
    step=1
)
st.session_state.years = (yearmin, yearmax)
ratingmin, ratingmax = st.slider(
    "Select rating range",
    min_value=float(df2["Rating"].min()),
    max_value=float(df2["Rating"].max()),
    value=st.session_state.scores,
    step=0.5
)
st.session_state.scores = (ratingmin, ratingmax)
filtered_df2 = df2[
    (df2["Year"] >= yearmin) & (df2["Year"] <= yearmax) &
    (df2["Rating"] >= ratingmin) & (df2["Rating"] <= ratingmax)
]
filtered_df2 = filtered_df2.copy()
filtered_df2["Rating"] = filtered_df2["Rating"].apply(lambda x: round(x*2)/2)
fig = px.scatter(
    filtered_df2,
    x="Year",
    y="Rating",
    hover_data=["Name"],
    width=800,
    height=400
)
st.plotly_chart(fig)
"""
This graph adds on to the last one by importing my actual letterboxd data. \n
The user can select a range of decades and scores to look at. \n
Enjoy these recommendations!
"""
