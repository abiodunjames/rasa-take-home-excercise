from flask import request
from flask_restx import Resource
from app.main.util.dto import ConversationDto

from app.main.util.decorator import admin_token_required
from app.main.service.conversation_service import get_all_conversations

conversation = ConversationDto.conversation
api = ConversationDto.api

@api.route('/')
@api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
class ConversationList(Resource):
    @api.doc('list_all_conversations')
    @admin_token_required
    @api.marshal_list_with(conversation, envelope='data')
    def get(self):
        """List all saved conversations"""
        return get_all_conversations()



