# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from weather_data import getweather
import os
import asyncio

class ActionGetWeather(Action):
    """ Return today's weather forecast"""
    
    def name(self):
          return "action_get_weather"

    def run(self, dispatcher, tracker, domain):
        city = tracker.get_slot('location')
        
        #api_token = <YOUR_API_TOKEN>
        
        #url = "https://api.openweathermap.org/data/2.5/weather"
        
        #payload = {"q": city, "appid": api_token, "units": "metric", "lang": "en"}
        
        #response = requests.get(url, params=payload)
        
        print('llega aca')
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        
        response =  getweather(city)     #           asyncio.run(getweather(city))
     
        #if response.ok:
        #    description = response.json()["weather"][0]["description"]
        #    temp = round(response.json()["main"]["temp"])
        #    city = response.json()["name"]
        #    msg = f"The current temperature in {city} is {temp} degree Celsius. Today's forecast is {description}"
        #else:
        #    msg = "I'm sorry, an error with the requested city as occured."
        #    dispatcher.utter_message(msg)
        temp = response.current.temperature

        msg = f"The current temperature in {city} is {temp} degree Celsius."  
        
        dispatcher.utter_message(msg)

        #return response
        return [SlotSet("location", None)]


class GreetAction(Action):

    def name(self):

        return "utter_greet"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message("Hey! How are you?")

    
        return []

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
