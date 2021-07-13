# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import requests
from requests.exceptions import HTTPError

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, ActionExecuted, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.parser import get_entity_details

#
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


class ActionCheckStatistics(Action):
    """Check country covid statistics"""

    def name(self) -> Text:
        return "action_check_statistics"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        location = get_entity_details(tracker, "location")
        if location:
            location = location.get("value").lower()
        else:
            location = "rwanda"
            # dispatcher.utter_message(text="For which country would you like to get its statistics?")

        print("location===", location)

        try:
            url = "https://disease.sh/v3/covid-19/all" if location == "world" else "https://disease.sh/v3/covid-19/countries/" + location
            res = requests.get(url)
            jsonResult = res.json()
            todayCases = str(jsonResult["todayCases"])
            totalCases = str(jsonResult["cases"])

            responseVars = {
                "number": todayCases,
                "location": location.capitalize(),
                "total": totalCases,
            }

            dispatcher.utter_message(response="utter_statistics", **responseVars)

        except HTTPError as httpError:
            dispatcher.utter_message(f"HTTP error occurred: {httpError}")
        except Exception as err:
            dispatcher.utter_message(f"Other error occurred: {err}")

        return []


# class ActionCheckWorldStatistics(Action):
#     """Check world covid statistics"""

#     def name(self) -> Text:
#         return "action_check_world_statistics"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:

#         # slots = {"number": None, "total": None}

#         try:
#             url = "https://disease.sh/v3/covid-19/all"
#             res = requests.get(url)
#             jsonResult = res.json()
#             todayCases = str(jsonResult["todayCases"])
#             totalCases = str(jsonResult["cases"])

#             # slot["number"] = todayCases
#             # slot["total"] = totalCases

#             responseVars = {
#                 "number": todayCases,
#                 "location": "the world",
#                 "total": totalCases,
#             }

#             dispatcher.utter_message(response="utter_statistics", **responseVars)

#         except HTTPError as httpError:
#             dispatcher.utter_message(f"HTTP error occurred: {httpError}")
#         except Exception as err:
#             dispatcher.utter_message(f"Other error occurred: {err}")

#         return []


# class ActionCheckCountryStatistics(Action):
#     """Check country covid statistics"""

#     def name(self) -> Text:
#         return "action_check_country_statistics"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:

#         location = get_entity_details(tracker, "country").get("value")
#         location = location.lower()

#         print("location===", location)

#         try:
#             url = "https://disease.sh/v3/covid-19/countries/" + location
#             res = requests.get(url)
#             jsonResult = res.json()
#             todayCases = str(jsonResult["todayCases"])
#             totalCases = str(jsonResult["cases"])

#             responseVars = {
#                 "number": todayCases,
#                 "location": location.capitalize(),
#                 "total": totalCases,
#             }

#             dispatcher.utter_message(response="utter_statistics", **responseVars)

#         except HTTPError as httpError:
#             dispatcher.utter_message(f"HTTP error occurred: {httpError}")
#         except Exception as err:
#             dispatcher.utter_message(f"Other error occurred: {err}")

#         return []
