import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="View Query Insights", page_icon="📈")


st.title("Location Queries Evolution")
st.write("This chart shows the number of queries for each location")


file = './query_insights.csv'
@st.cache_data
def load_data(file):
    
    return pd.read_csv(file, sep=',')

data = load_data(file)

def locationQueries(query_data):

    

    locations_query = query_data.groupby(['date','location']).size().to_frame('numberOfQueries')

    locations_query['totalQueries'] = locations_query.groupby('location')['numberOfQueries'].cumsum()


    locations_query = locations_query.reset_index()
    fig = px.line(locations_query, x= locations_query["date"], y="totalQueries", color='location',  markers=True)
    fig.update_layout(xaxis=dict(tickformat="%d-%m-%Y"))

    fig.update_xaxes(tickangle=0,
                 tickmode = 'array',
                 tickvals = query_data['date'].unique())
                 #ticktext= [d.strftime('%Y-%m-%d') for d in chart_data['date'].unique() ])
  
    return st.plotly_chart(fig, theme=None)


def topIntents(query_data):


    weather_query = query_data.groupby(['date','intent']).size().to_frame('WeatherQueries')
    weather_query = weather_query.reset_index()

    dates = list(weather_query['date'].unique())

    date_selected = st.selectbox('Choose date to check Top Weather Queries',
             dates)

    day_weather_query = weather_query[weather_query['date'] == date_selected]

    chart = px.bar(day_weather_query, x="WeatherQueries", y="intent", color='location', orientation='h',
             hover_data=["WeatherQueries"],
             height=200,
             title='Weather Queries by Location & Date')
    
    return chart.show()



locationQueries(data)
topIntents(data)
