# Placeholder actions file for Rasa actions server.
# Add custom actions here if you want to fetch live data.
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback_handler"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I'm sorry, I couldn't process that. Please contact the county office.")
        return []
