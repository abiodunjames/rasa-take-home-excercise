from app.main.model.conversation import Conversation
from app.main import db
import datetime

SEED_REQUEST = "hey"
SEED_RESPONSE = "howdy"


def seed_conversation():
    """
    Stores conversation
    """
    conver = Conversation(
        request=SEED_REQUEST,
        response=SEED_RESPONSE,
        generated_on=datetime.datetime.utcnow(),
    )
    db.session.add(conver)
    db.session.commit()
