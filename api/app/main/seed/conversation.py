from app.main.model.conversation import Conversation
from app.main import db
import datetime

USER_MESSAGE = "hey"
BOT_RESPONSE = "howdy"


def seed_conversation() -> None:
    """
    Stores conversation
    """
    conver = Conversation(
        message=USER_MESSAGE,
        response=BOT_RESPONSE,
        generated_on=datetime.datetime.utcnow(),
    )
    db.session.add(conver)
    db.session.commit()
