import datetime
import os
from typing import Dict, List

import requests
from app.main import db
from app.main.model.conversation import Conversation
from flask import request


def save_new_conservation(
    user_chat: str, bot_response: str, sender: str
) -> Conversation:
    """
    Note: Saving conversation history in the database here is a bad idea because:

    1. Rasa [tracker store](https://rasa.com/docs/rasa/api/tracker-stores/) handles that already
    2. It increases latency.
    3. It's a bad design

    I did it anyway because because the `/conversations` endpoint [documented here](https://rasa.com/docs/rasa-x/api/rasa-x-http-api/#operation/getConversations)
    does not work for me, and I do not have enough time to dig deeper or reach out to rasa developers
    """
    conversation = Conversation(
        message=bot_response,
        response=user_chat,
        sender=sender,
        generated_on=datetime.datetime.utcnow(),
    )
    save_changes(conversation)

    return conversation


def get_all_conversations() -> List[Conversation]:
    """
    Get all conversations saved in the database
    """
    return Conversation.query.all()


def predict_response():
    """ Call inference server for prediction """

    inference_endpoint = os.getenv(
        "INFERENCE_ENDPOINT", "http://inference_server:5005/webhooks/rest/webhook"
    )
    data = request.get_json()
    prediction = requests.post(inference_endpoint, json=data)
    response = prediction.json()
    bot_response = None
    if response:
        response = response[0]
        bot_response = response["text"] or None

    # TODO: Refactor the line below. See my comment above
    save_new_conservation(data["message"], bot_response, data["sender"])

    return response


def save_changes(data: Conversation) -> None:
    db.session.add(data)
    db.session.commit()
