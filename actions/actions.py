from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted


class ActionGreetUser(Action):
    """ Prevent intent from affecting chat history """

    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_greet")
        return [UserUtteranceReverted()]


class ActionDefaultAskAffirmation(Action):
    """ Asks for an affirmation of the intent if threshold is not met """

    def name(self):
        return "action_out_of_scope"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_out_of_scope")
        return []
