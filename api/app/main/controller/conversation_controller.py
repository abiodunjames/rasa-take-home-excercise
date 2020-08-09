from flask import request, jsonify
from flask_restx import Resource
from app.main.util.dto import ConversationDto

from app.main.util.decorator import admin_token_required
from app.main.service.conversation_service import get_all_conversations
from app.main.model.conversation import Conversation
from typing import List
import requests
import os
import sys

conversation = ConversationDto.conversation
api = ConversationDto.api


@api.route("/")
@api.doc(
    params={"Authorization": {"in": "header", "description": "An authorization token"}}
)
class ConversationList(Resource):
    @api.doc("list_all_conversations")
    @admin_token_required
    @api.marshal_list_with(conversation, envelope="data")
    def get(self) -> List[Conversation]:
        """List all saved conversations"""
        return get_all_conversations()


@api.route("/webhook")
class ConversationWebhook(Resource):
    """
       Predict response
    """

    @api.doc("conversation webhook")
    @api.expect(conversation, validate=True)
    def post(self):
        # Todo: Refactor this block later
        inference_endpoint = os.getenv(
            "INFERENCE_ENDPOINT", "http://inference_server:5005/webhooks/rest/webhook"
        )
        data = request.get_json()
        prediction = requests.post(inference_endpoint, json=data)
        response = prediction.json()

        return response, 200
