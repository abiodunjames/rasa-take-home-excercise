import datetime
import os
from typing import Dict, List

import requests
from app.main import db
from app.main.model.conversation import Conversation
from flask import request


def save_new_conservation(user_chat: str, bot_response: str) -> Conversation:
    """
    Store chat conversation response in the databse
    """
    conversation = Conversation(
        message=bot_response,
        response=user_chat,
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
    save_new_conservation(data["message"], bot_response)

    return response


def save_changes(data: Conversation) -> None:
    db.session.add(data)
    db.session.commit()
