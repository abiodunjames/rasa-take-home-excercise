import json
import unittest

from app.main import db
from app.main.model.user import User
from app.main.seed.conversation import BOT_RESPONSE, USER_MESSAGE, seed_conversation
from app.test.base import BaseTestCase


def get_conversation_list(self):
    seed_conversation()
    admin_user_id = 1  # seeded in base.py
    admin = User.query.filter_by(id=admin_user_id).first()
    token = User.encode_auth_token(admin)
    return self.client.get(
        "/conversations/", headers={"Authorization": token.decode("utf-8")}
    )


class TestConversationBlueprint(BaseTestCase):
    def test_admin_user_get_all_conversations(self):
        """ Test admin user can get a conversation list """
        get_conversation_list(self)
        with self.client:
            response = get_conversation_list(self)
            json_response = json.loads(response.data.decode())
            data = json_response["data"]
            self.assertTrue(data[0]["message"] == USER_MESSAGE)
            self.assertTrue(data[0]["response"] == BOT_RESPONSE)
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 200)

    def test_non_admin_user_can_not_get_conversation(self):
        pass

    def test_un_authorized_user_can_not_get_conversation(self):
        pass


if __name__ == "__main__":
    unittest.main()
