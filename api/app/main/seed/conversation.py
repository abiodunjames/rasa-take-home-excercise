import datetime

from app.main import db
from app.main.model.conversation import Conversation

USER_MESSAGE = "hey"
BOT_RESPONSE = "howdy"


def seed_conversation() -> None:
    """
    Stores conversation
    """
    conver = Conversation(
        message=USER_MESSAGE,
        response=BOT_RESPONSE,
        sender="test_sender",
        generated_on=datetime.datetime.utcnow(),
    )
    db.session.add(conver)
    db.session.commit()
