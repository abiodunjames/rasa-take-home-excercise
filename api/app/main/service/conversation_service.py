import datetime
from typing import List

from app.main import db
from app.main.model.conversation import Conversation


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


def save_changes(data: Conversation) -> None:
    db.session.add(data)
    db.session.commit()
