from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted


class ActionGreetUser(Action):
    """ Prevent intent from affecting chat history """

    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_greet")
        return [UserUtteranceReverted()]
