import datetime
import unittest

from app.main import db
from app.main.model.conversation import Conversation
from app.main.service.conversation_service import (
    get_all_conversations,
    save_new_conservation,
)
from app.test.base import BaseTestCase


class TestConversationService(BaseTestCase):
    def test_save_new_conversation(self):
        bot_response = "Howdy"
        user_chat = "Hey"
        result = save_new_conservation(user_chat, bot_response)
        self.assertTrue(isinstance(result, Conversation))

    def test_get_all_conversations(self):
        chat = Conversation(
            message="hey", response="howdy", generated_on=datetime.datetime.utcnow()
        )
        db.session.add(chat)
        db.session.commit()
        results = get_all_conversations()
        assert len(results) == 1
        assert results[0].message == "hey"
        assert results[0].response == "howdy"


if __name__ == "__main__":
    unittest.main()
