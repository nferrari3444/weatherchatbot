import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="View Query Insights", page_icon="📈")

st.markdown("Insights")
st.sidebar.header("Plotting Demo")

file = './query_insights.csv'
@st.cache_data
def load_data(file):
    
    return pd.read_csv(file, sep=',')

chart_data = load_data(file)

locations_query = chart_data.groupby(['date','location']).size().to_frame('numberOfQueries')
print('---------------------')
locations_query = locations_query.reset_index()
fig = px.line(locations_query, x= locations_query["date"], y="numberOfQueries", color='location',  markers=True)

st.plotly_chart(fig, theme=None)
# print('After group by ', locations_query)
# locations_query = locations_query.reset_index()
# #locations_query = locations_query.rename(columns= {0:'numberOfQueries'})
# #location_query = locations_query.reset_index()

# # res = df.pivot(index='date', columns='name', values='quantity')
# locations_query = locations_query.sort_values('numberOfQueries', ascending=False)

# print('locations_query before pivot ', locations_query)

# locations_query = locations_query.pivot(index='date', columns='location', values='numberOfQueries')

# print('locations after pivot', locations_query)

# st.title("Location Users Queries Plot")

# st.write("This chart shows the number of queries for each location")
# locations_query = locations_query.reset_index()
# fig = px.line(locations_query, x="date", y= locations_query.columns[1:], title="Popular locations weather queries")

# st.plotly_chart(fig)


