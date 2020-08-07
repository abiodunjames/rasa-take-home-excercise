import datetime
from app.main import db
from app.main.model.conversation import Conversation

def save_new_conservation(user_chat, bot_response):
    """
    Store chat conversation response in the databse
    """
    conversation = Conversation(
        request=bot_response,
        response=user_chat,
        generated_on=datetime.datetime.utcnow()
    )
    save_changes(conversation)

    return conversation

def get_all_conversations():
    """
    Get all conversations saved in the database
    """
    return Conversation.query.all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()