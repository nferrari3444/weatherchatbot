import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="View Query Insights", page_icon="📈")

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


def topIntents(query_data, date_selected):


    weather_query = query_data.groupby(['date','intent','location']).size().to_frame('WeatherQueries')
    weather_query = weather_query.reset_index()   

    if date_selected == 'All Period':
        weather_query_period = weather_query
    else:
        weather_query_period = weather_query[weather_query['date'] == date_selected]

    weather_query_period = weather_query_period.sort_values('WeatherQueries', ascending=False)
    chart = px.bar(weather_query_period, x="WeatherQueries", y="intent", color='location', orientation='h',
        
             height=400,
             title='Weather Queries by Location & Date')
    chart.update_layout(yaxis={'categoryorder':'total ascending'}) # add only this line
    #fig=px.bar(df,x='total_bill',y='day', orientation='h')
    st.write(chart)


st.title("Location Queries Evolution")
st.write("Number of queries for each location over time")

st.sidebar.text_area(
    "Get relevant insights",
    "Based in the graph on the right side, uses can get insights and valuable information "
    "about query trends for the relevant cities, as well as the behaviour of the weather"
    "among the cities", height=200
    )


locationQueries(data)



st.title("Queries Breakdown by Location")
st.write("Show the distribution of each weather query regard locations")

dates = list(data['date'].unique())
dates.insert(0, 'All Period')

date_selected = st.selectbox('Choose date to check Top Weather Queries',
             dates)


topIntents(data, date_selected)
