from typing import List

import requests
from app.main.model.conversation import Conversation
from app.main.service.conversation_service import (
    get_all_conversations,
    predict_response,
)
from app.main.util.decorator import admin_token_required
from app.main.util.dto import ConversationDto
from flask import jsonify, request
from flask_restx import Resource

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
        return get_all_conversations(), 200


@api.route("/webhook")
class ConversationWebhook(Resource):
    @api.doc("conversation webhook")
    @api.expect(conversation, validate=True)
    def post(self):
        """ Predict response """
        response = predict_response()
        return response, 200
