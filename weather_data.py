import python_weather
import streamlit as st
import asyncio
import aiohttp
import os
#from test import classify


async def getweather(location):
#def getweather():
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
 # conn = aiohttp.TCPConnector(verify_ssl=False)
  async with python_weather.Client(unit=python_weather.METRIC) as client:
    
 #   client =  python_weather.Client(unit=python_weather.METRIC)
    # fetch a weather forecast from a city

      location =  st.session_state.location if st.session_state.location != '' else "Berlin" 
 
      weather = await client.get(location)
    #weather = client.get(location)
    
  #  st.write('location is:', location)
     # print('intent is:', user_query_intent[0])
    
      print('weather methods' , dir(weather))
      
      #intent = user_query_intent[0]  
    
      #map_intent_api_data = {'temperature': 'Current Temperature is {}'.format(weather.current.temperature),
      #                    'humidity' : 'The humidity is {}'.format(weather.current.humidity),
      #                    'pressure': 'Currently the pressure is about {}'.format(weather.current.pressure),
      #                    'precipitation': 'There are {} probabilities of precipitations'.format(weather.current.precipitation),
      #                    'wind': 'The wind direction is {}'.format(weather.current.wind_direction),    
      #                    'visibility': 'The current visibility is {}'.format(weather.current.visibility),
      #                    'kind': 'There is {}'.format(weather.current.kind),
      #                    'description': 'Currently the weather is {}'.format(weather.current.description),
      #                    'goodbye': "Can I help with more information?",
      #                    'greeting':  "Hello, Im doing well, hope that you are having a great day" }
                                                                                                    
      #data = map_intent_api_data[intent]

      print('weather current methods', dir(weather.current))
      # returns the current day's forecast temperature (int)
      print("the temperature in {} is {}".format(location,weather.current.temperature))
      print('description', weather.current.description)
      print('feels_like', weather.current.feels_like)
      print('humidity', weather.current.humidity)
      print('kind', weather.current.kind)
      print('precipitation', weather.current.precipitation)
      print('pressure',weather.current.pressure)
      print('temperature', weather.current.temperature)
      print('ultraviolet', weather.current.ultraviolet)
      print('visibility', weather.current.visibility)
      print('wind_direction', weather.current.wind_direction)
      print('wind_speed', weather.current.wind_speed)

  #st.session_state.messages.append({"role": "assistant", "content": data, "intent": intent, "location": location})

 
  return  weather