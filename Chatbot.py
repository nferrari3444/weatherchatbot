import python_weather
import streamlit as st
import asyncio
import aiohttp
import os
import requests
import json
from streamlit_extras.annotated_text import annotated_text 
from streamlit_extras.tags import tagger_component 
import datetime
from datetime import timedelta
from utils import query_records

st.title("Welcome to the Weather Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "queries" not in st.session_state:
    st.session_state.queries = []

currentDate = datetime.datetime.today().strftime('%Y-%m-%d')

with st.sidebar:
   # st.write('Most commond searchs for the Weather bot')
    tagger_component('Most Frequent Searchs:', 
                     ['weather','temperature','humidity','wind','weather forecast',
                      'precipitation', 'tomorrow temperature'])

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



async def getweather(location, intent, forecast_next_day, forecast_day):

  async with python_weather.Client(unit=python_weather.METRIC) as client:
     
      weather = await client.get(location)

      if forecast_next_day:
        year = datetime.datetime.now().year  
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        current_date = datetime.date(year, month, day)

        for forecast in weather.forecasts:
          print('forecast is ', forecast.date)
          if forecast.date - timedelta(1) == current_date:
            print('The temperature for tomorrow in {} will be {} degrees Celcius'.format(location, forecast.temperature))
            
            data = 'The temperature for tomorrow in {} will be {} degrees Celcius'.format(location, forecast.temperature)
            
          #  st.session_state.messages.append({"role": "assistant", "content": data, "intent": intent, "location": location})
            query_info = {'date': currentDate, 'intent':intent, 'location':location}
            query_records(query_info)
            st.session_state.queries.append({'date': currentDate, 'intent':intent, 'location':location})

            return data 

      if forecast_day:
         currentHour = datetime.datetime.now().time().hour 

         for forecast in weather.forecasts:
            for hourly in forecast.hourly:
                
                if  hourly.time.hour -  currentHour == 6:
                    description = hourly.description
                    temperature = hourly.temperature
                    print('---------------------------------------------------------------------')
                    print('The weather for the next 6 hours in {} will be {} with a temperature of {}'.format(location, description,temperature))
      
                   # st.session_state.messages.append({"role": "assistant", "content": data, "intent": intent, "location": location})
                    query_info = {'date': currentDate, 'intent':intent, 'location':location}
                    query_records(query_info)
                    st.session_state.queries.append({'date': currentDate, 'intent':intent, 'location':location})
                    
                    data = 'The weather for the next 6 hours in {} will be {} with a temperature of {}'.format(location, description,temperature)

                    return data
      else:
            map_intent_api_data = {'temperature_city': 'The Current Temperature in {} is {} degrees Celcius'.format(location, weather.current.temperature),
                          'humidity_city' : 'The humidity in {} is {} %'.format(location, weather.current.humidity),
                          #'pressure': 'Currently the pressure is about {}'.format(weather.current.pressure),
                          #'precipitation': 'There are {} probabilities of precipitations'.format(weather.current.precipitation),
                          'wind_city': 'The wind direction in {} is {} with a velocity of {} km/h'.format(location, weather.current.wind_direction, weather.current.wind_speed),    
                          #'visibility': 'The current visibility is {}'.format(weather.current.visibility),
                          #'kind': 'There is {}'.format(weather.current.kind),
                          'weather_city': 'Currently the weather in {} is {}'.format(location, weather.current.description)}
                          
                          #'goodbye': "Can I help with more information?",
                          #'greeting':  "Hello, Im doing well, hope that you are having a great day" }
                                                                                                    
            data = map_intent_api_data[intent]
            #data = 'The temperature in {} is {} degrees celcius'.format(location, weather.current.temperature)  
     
           
            #st.session_state.messages.append({"role": "assistant", "content": data, "intent": intent, "location": location})

 
            return  data

def modelResponse(userInput):

   

    payload = {"sender": "Rasa","text": userInput}

    url_intent = 'http://localhost:5005/model/parse'
    
    #url = 'http://localhost:5005/webhooks/rest/webhook'

    print('userInput is', userInput)
    
    sendInput = requests.post(url_intent, json = payload, headers = {'content-type': 'application/json'})

    data = sendInput.json()
    print('data is', data)
    return data
  

def botResponse(modelData, userInput):
    
    forecast_day = False
    forecast_next_day = False

    intent = modelData['intent']['name']
    print('intent is', intent)
    if intent == 'weather_city' or intent == 'weather_next_day_forecast_city'  or intent == 'weather_day_forecast_city' or intent == 'humidity_city' or intent == 'wind_city' or intent == 'temperature_city':
        location = modelData['entities'][0]['value']
        
        print('llega aca con el intent {}'.format(intent))

        if intent == 'weather_next_day_forecast_city':
            forecast_next_day = True
        if intent == 'weather_day_forecast_city':
            forecast_day = True

        query_info = {'date': currentDate, 'intent':intent, 'location':location}
        query_records(query_info)
        st.session_state.queries.append({'date': currentDate, 'intent': intent, 'location':location})

        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        return asyncio.run(getweather(location, intent, forecast_next_day, forecast_day))
        
        
        #st.session_state.messages.append({"role": "user", "content": userInput, "intent": intent, "location": location})

    else:

        try:

            payload = {"sender": "me",  'message': userInput, 'token': "None"}

            # st.session_state.messages.append({"role": "user", "content": userInput, "intent": intent})

            url = 'http://localhost:5005/webhooks/rest/webhook'

            x = requests.post(url, json = payload, headers = {'content-type': 'application/json'})

            data = x.json()
   
            response = data[0]['text']

        except IndexError:
            response = 'Sorry, the assistent answer questions about weather in main cities. Make the question again please!'
        
        #st.session_state.messages.append({"role": "assistant", "content": response, "intent": intent})

        return response



headers = ['Name', 'Age', 'Website']
nik = {'Name': 'Nik', 'Age': 34, 'Website': 'datagy.io'}
kate = {'Website': 'google', 'Name': 'Kate', 'Age': 33}




if __name__ == '__main__':

    
    if inputUser:= st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(inputUser)
            st.session_state.messages.append({"role": "user", "content": inputUser}) 
            

            data = modelResponse(inputUser)
            

        with st.chat_message("assistant"):
            response = botResponse(data, inputUser)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response}) 

